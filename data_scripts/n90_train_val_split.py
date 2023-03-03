from sklearn.model_selection import train_test_split
import argparse
import h5py
import numpy as np


DTYPES = {'data/y': 'int8',
          'data/X': 'float16',
          'data/sample_weights': 'int8',
          'data/gene_lengths': 'uint32',
          'data/phases': 'int8',
          'data/seqids': 'S50',
          'data/species': 'S25',
          'data/start_ends': 'int64',
          'data/transitions': 'int8',
          'data/err_samples': 'bool',
          'data/fully_intergenic_samples': 'bool',
          'data/is_annotated': 'bool',
          'evaluation/rnaseq_coverage': 'int',
          'evaluation/rnaseq_spliced_coverage': 'int',
          'rnaseq_meta/bam_files': 'S512'}


def split_coords_by_N90(genome_coords, val_fraction):
    """Length stratifying split of given coordinates into a train and val set.

    Coordinates are first split by the N90 of the genome_coords[:, 1] (intended subsequence count). Then
    the smaller and larger coordinates are individually split into train and val sets.

    Parameters
    ----------
    genome_coords : iter[(str, int)]
        coord_id, coord_subsequence_count for all coordinates / sequences
    val_fraction : float
        target fraction of coordinates to assign to val set

    Returns
    -------
    (list[str], list[str])
        coord_ids assigned to training and validation, respectively
    """
    def N90_index(coords):
        len_90_perc = int(sum([c[1] for c in coords]) * 0.9)
        len_sum = 0
        for i, coord in enumerate(coords):
            len_sum += coord[1]
            if len_sum >= len_90_perc:
                return i

    genome_coords = sorted(genome_coords, key=lambda x: x[1], reverse=True)

    train_coord_ids, val_coord_ids = [], []
    n90_idx = N90_index(genome_coords) + 1
    coord_ids = [c[0] for c in genome_coords]
    for n90_split in [coord_ids[:n90_idx], coord_ids[n90_idx:]]:
        if len(n90_split) < 2:
            # if there is no way to split a half only add to training data
            train_coord_ids += n90_split
        else:
            genome_train_coord_ids, genome_val_coord_ids = train_test_split(n90_split,
                                                                            test_size=val_fraction)
            train_coord_ids += genome_train_coord_ids
            val_coord_ids += genome_val_coord_ids
    return train_coord_ids, val_coord_ids


def copy_structure(h5_in, h5_out):
    """copy structure of one h5 file to another insofar as it's just group/dataset(s)"""
    groups = h5_in.keys()
    # setup all groups if they don't exist
    for g in groups:
        try:
            h5_out[g]
        except KeyError:
            h5_out.create_group(g)

    # setup all datasets within groups if they don't exist
    for g in groups:
        for ds in h5_in[g].keys():
            try:
                h5_out[g][ds]
            except KeyError:
                dat = h5_in[g][ds]
                shape = list(dat.shape)
                shape[0] = 0  # create it empty
                shuffle = len(shape) > 1
                h5_out.create_dataset(f'/{g}/{ds}', shape=shape,
                                      maxshape=tuple([None] + shape[1:]),
                                      chunks=tuple([1] + shape[1:]),
                                      dtype=DTYPES[f'{g}/{ds}'],
                                      compression='gzip',  #dat.compression
                                      shuffle=shuffle)

    # attributes are things like the commits and paths, that won't be split
    # so copy entirely
    for key, val in h5_in.attrs.items():
        if key not in h5_out.attrs.keys():
            h5_out.attrs.create(key, val)


def copy_some_data(h5_in, h5_out, datakey, mask, start_i, end_i):
    """basically appends h5_in[datakey][start_i:end_i][mask] to h5_out[datakey]"""
    if end_i is None:
        end_i = len(h5_in[datakey])

    samples = np.array(h5_in[datakey][start_i:end_i])

    if mask is not None:
        samples = samples[mask]

    old_len = len(h5_out[datakey])
    h5_out[datakey].resize(old_len + len(samples), axis=0)
    h5_out[datakey][old_len:] = samples


def copy_groups_recursively(h5_in, h5_out, groups, mask, start_i, end_i):
    """basically appends h5_in[*][start_i:end_i][mask] to h5_out[*], where * loops through all groups/datasets"""
    for g in groups:
        for key in h5_in[g].keys():
            copy_some_data(h5_in, h5_out, f'{g}/{key}', mask, start_i, end_i)


def main(args):
    h5_in = h5py.File(args.h5_to_split, 'r')
    train_out = h5py.File(args.output_pfx + 'training_data.h5', 'w')
    val_out = h5py.File(args.output_pfx + 'validation_data.h5', 'w')

    # setup all shared info for output files
    for h5_out in [train_out, val_out]:
        copy_structure(h5_in, h5_out)
        # also copy the entirety of the metadata to both outputs
        meta_groups = [g for g in h5_in.keys() if g.endswith('_meta')]
        copy_groups_recursively(h5_in, h5_out, meta_groups, mask=None, start_i=0, end_i=None)

    # identify what goes to train vs val
    input_seqids = h5_in['data/seqids']
    coord_ids, coord_subsequence_counts = np.unique(input_seqids, return_counts=True)
    train_coord_ids, val_coord_ids = split_coords_by_N90(zip(coord_ids, coord_subsequence_counts),
                                                         val_fraction=args.val_fraction)
    print(f'assigning {len(train_coord_ids)} and {len(val_coord_ids)} coordinates to train and val respectively')
    train_mask = np.isin(input_seqids, train_coord_ids)
    val_mask = np.isin(input_seqids, val_coord_ids)

    # go through in mem friendly chunks, writing data to each split
    not_meta_groups = [g for g in h5_in.keys() if not g.endswith('_meta')]
    by = args.write_by // h5_in['data/X'].shape[1]
    end = len(h5_in['data/X'])
    for i in range(0, end, by):
        print(f'{i} / {end}')
        sub_t_mask = train_mask[i:i + by]
        sub_v_mask = val_mask[i:i + by]

        if np.any(sub_t_mask):
            copy_groups_recursively(h5_in, train_out, not_meta_groups, sub_t_mask, i, i + by)
        if np.any(sub_v_mask):
            copy_groups_recursively(h5_in, val_out, not_meta_groups, sub_v_mask, i, i + by)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--h5-to-split', type=str, required=True,
                        help='h5 file that will be split by coordinate so that both coordinates > N90 and < N90'
                             'are where possible represented in both train and val')
    parser.add_argument('-o', '--output-pfx', type=str, default='./',
                        help='literally prefixed to training_data.h5 and validation_data.h5; '
                             'recommendation: an existing h5 data directory')
    parser.add_argument('--val-fraction', type=float, default=0.2, help='validation set fraction')
    parser.add_argument('--write-by', type=int, default=500_000,
                        help='max base pairs to read (into RAM)/write at once')

    args = parser.parse_args()

    main(args)
