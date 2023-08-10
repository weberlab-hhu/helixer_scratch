#! /usr/bin/env python3
import time
import h5py
import argparse
import numpy as np
import datetime
from n90_train_val_split import copy_structure, copy_groups_recursively


parser = argparse.ArgumentParser()
parser.add_argument('--predictions', type=str, required=True, help='raw h5 Helixer predictions')
parser.add_argument('--h5-to-filter', type=str, required=True, help='h5 file that will be filtered to where the'
                                                                    'references there in align most confidently with'
                                                                    'predictions')
parser.add_argument('--output-file', type=str, required=True)
parser.add_argument('--keep-fraction', type=float, default=0.5, help='keep this fraction of total')
parser.add_argument('--dry-run', action='store_true', help='Just output what would be done')
parser.add_argument('--write-by', type=int, default=6_000_000, help='max base pairs to read (into RAM)/write at once')
args = parser.parse_args()


def to_stratification_quantiles(fraction_intergenic, qbreaks=None):
    """converts raw input to low resolution rank (equal membership bins)"""
    if qbreaks is None:
        qbreaks = tuple([x / 6 for x in range(1, 6)])

    quartiles = np.quantile(fraction_intergenic, qbreaks)
    # basically the index any item in fraction_intergenic would need to slip it sorted into quartiles
    quant_indices = np.searchsorted(quartiles, fraction_intergenic)
    return quant_indices


def closest_matches(h5_in, predictions, n_samples):
    ds = h5_in['data/y']
    shape = [ds.shape[x] for x in [0, 2]]  # [N, 4] where N varies from ~100-100k with genome length
    by = 100
    all_dists = np.zeros(shape=shape)
    all_counts = np.zeros(shape=shape)
    for i in range(0, ds.shape[0], by):
        y = ds[i:(i + by)]
        preds = predictions['predictions'][i:(i + by)]
        # we want to select examples where the predictions are
        # a) confident, and
        # b) agree with reference, and
        # c) have a fair distribution of each class (i.e. not just intergenic, which is generally easiest)
        # d) are counted by basepair, ignoring padding

        # for (d) zero-out predictions where y is padded (zeros)
        padding = np.logical_not(np.sum(y, axis=2).astype(bool))
        preds[padding] = 0.
        # for a - c, track distance and counts
        distance = np.abs(y - preds)
        all_dists[i:(i + by)] = np.sum(distance, axis=1)
        all_counts[i:(i + by)] = np.sum(y, axis=1)

    # summarize down to one value per subsequence
    average_distances = np.sum(all_dists, axis=1) / np.sum(all_counts, axis=1)

    # normalized_dist still favors pure intergenic so just use stratification to force class distribution
    ig_ranks = to_stratification_quantiles(all_counts[:, 0] / np.sum(all_counts, axis=1))
    unique_ranks = np.unique(ig_ranks)
    n_each = n_samples // len(unique_ranks)
    argsort_list = []
    dist_list = []
    # find lowest distance within each intergenic fraction rank
    for rnk in unique_ranks:
        avd = np.copy(average_distances)
        avd[np.logical_not(ig_ranks == rnk)] = np.inf  # all other ig ranks will not be selected
        ag = np.argsort(avd)
        argsort_list.append(ag[:n_each])
        dist_list.append(avd[ag[n_each]])

    # indexes of subsequences with lowest distances
    argsort = np.concatenate(argsort_list)
    return argsort, dist_list


def main(args):
    h5_in = h5py.File(args.h5_to_filter, 'r')
    predictions = h5py.File(args.predictions, 'r')

    start_time = time.time()
    dsets_in = h5_in['data']

    n_samples_source, chunk_size = dsets_in['X'].shape[0:2]
    max_n_chunks = int(args.write_by / chunk_size)

    n_samples = int(n_samples_source * args.keep_fraction)
    assert 0 < n_samples < n_samples_source, '--keep-fraction should be set so that the h5 file is _downsampled_'
    samples_idx, furthest_distance = closest_matches(h5_in, predictions, n_samples)
    samples_idx = sorted(samples_idx)
    mask = np.zeros(shape=(h5_in['data/X'].shape[0],),
                    dtype=bool)
    mask[samples_idx] = True

    print(f'selecting {len(samples_idx)} with average '
          f'normalized distances below in each genic proportion ranking {furthest_distance}', flush=True)
    if not args.dry_run:
        h5_out = h5py.File(args.output_file, 'w')
        skip_groups = copy_structure(h5_in, h5_out)
        for si in range(0, h5_in['data/X'].shape[0], max_n_chunks):
            copy_groups_recursively(h5_in, h5_out, skip_arrays=skip_groups, start_i=si, end_i=si + max_n_chunks,
                                    mask=mask[si:si + max_n_chunks])

        h5_out.attrs['timestamp'] = str(datetime.datetime.now())
        for key, value in vars(args).items():
            h5_out.attrs[key] = str(value)
        h5_out.close()

    print(f'added {len(samples_idx)} / {n_samples_source} samples of normalized '
          f'distances less than {furthest_distance} in {time.time() - start_time:.2f} secs', flush=True)
    h5_in.close()
    print(f'closed {args.output_file}')


if __name__ == "__main__":
    main(args)
