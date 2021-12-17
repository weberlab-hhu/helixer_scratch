#! /usr/bin/env python3
import time
import h5py
import argparse
import numpy as np
import datetime
from helixer.export.exporter import HelixerExportController


parser = argparse.ArgumentParser()
parser.add_argument('--predictions', type=str, required=True, help='raw h5 Helixer predictions')
parser.add_argument('--h5-to-filter', type=str, required=True, help='h5 file that will be filtered to where the'
                                                                    'references there in align most confidently with'
                                                                    'predictions')
parser.add_argument('--output-file', type=str, required=True)
parser.add_argument('--keep-fraction', type=float, default=0.5, help='keep this fraction of total')
parser.add_argument('--dry-run', action='store_true', help='Just output what would be done')
parser.add_argument('--write-by', type=int, default=100_000_000, help='max base pairs to read (into RAM)/write at once')
args = parser.parse_args()


def closest_matches(h5_in, predictions, n_samples):
    ds = h5_in['data/y']
    by = 100
    all_dists = np.zeros(shape=(ds.shape[0],))
    for i in range(0, ds.shape[0], by):
        y = ds[i:(i + by)]
        preds = predictions['predictions'][i:(i + by)]
        # we want to select examples where the predictions are
        # a) confident, and
        # b) agree with reference
        distance = np.abs(y - preds)
        all_dists[i:(i + by)] = np.sum(distance, axis=(1, 2))
    argsort = np.argsort(all_dists)
    return argsort[:n_samples], all_dists[n_samples] / np.prod(ds.shape[1:])


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

    print(f'selecting {n_samples} with average distance below {furthest_distance}', flush=True)
    if not args.dry_run:
        h5_out = h5py.File(args.output_file, 'w')
        h5_out.create_group('data')
        for key in h5_in['data'].keys():
            for si in range(0, n_samples, max_n_chunks):
                samples = dsets_in[key][samples_idx[si:(si + max_n_chunks)]]
                if key not in h5_out['data'].keys():
                    HelixerExportController._create_dataset(h5_out, f'/data/{key}', samples, dsets_in[key].dtype)
                    dsets_out = h5_out['data']

                old_len = dsets_out[key].shape[0]
                dsets_out[key].resize(old_len + len(samples), axis=0)
                dsets_out[key][old_len:] = samples

        h5_out.attrs['timestamp'] = str(datetime.datetime.now())
        for key, value in vars(args).items():
            h5_out.attrs[key] = str(value)
        h5_out.close()

    print(f'added {n_samples} / {n_samples_source} samples of distance less than {furthest_distance} in {time.time() - start_time:.2f} secs', flush=True)
    h5_in.close()
    print(f'closed {args.output_file}')
