#! /usr/bin/env python3
import sys
import time
import h5py
import argparse
import numpy as np
import datetime
from helixer.export.exporter import HelixerExportController
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

    # prep to normalize so that each class has same average distance
    class_counts = np.sum(all_counts, axis=0)
    class_distances = np.sum(all_dists, axis=0)
    average_class_dist = class_distances / class_counts
    class_dist_weights = np.mean(average_class_dist) / average_class_dist
    # normalize and summarize down to one value per subsequence
    normalized_dist = np.sum(all_dists * class_dist_weights / class_counts, axis=1)
    # indexes of subsequences to sort by this distance
    argsort = np.argsort(normalized_dist)
    return argsort[:n_samples], normalized_dist[n_samples] / np.prod(ds.shape[1:])


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

    print(f'selecting {n_samples} with average normalized distance below {furthest_distance}', flush=True)
    if not args.dry_run:
        h5_out = h5py.File(args.output_file, 'w')
        copy_structure(h5_in, h5_out)
        groups = [key for key in h5_in.keys() if not key.endswith('_meta')]
        for si in range(0, h5_in['data/X'].shape[0], max_n_chunks):
            copy_groups_recursively(h5_in, h5_out, groups=groups, start_i=si, end_i=si + max_n_chunks,
                                    mask=mask[si:si + max_n_chunks])

        h5_out.attrs['timestamp'] = str(datetime.datetime.now())
        for key, value in vars(args).items():
            h5_out.attrs[key] = str(value)
        h5_out.close()

    print(f'added {n_samples} / {n_samples_source} samples of normalized '
          f'distance less than {furthest_distance} in {time.time() - start_time:.2f} secs', flush=True)
    h5_in.close()
    print(f'closed {args.output_file}')


if __name__ == "__main__":
    main(args)
