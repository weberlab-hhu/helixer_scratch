#! /usr/bin/env python3
import os
import time
import math
import h5py
import argparse
import numpy as np
import datetime
from helixer.export.exporter import HelixerExportController

parser = argparse.ArgumentParser()
parser.add_argument('--main-folder', type=str, default='', required=True,
                    help='Main single genome folder. Expects "test_data.h5" files inside subfolders.')
parser.add_argument('--output-file', type=str, default='./validation_data.h5')
parser.add_argument('--coefficient', type=float, default=1.0)
parser.add_argument('--exponent', type=float, default=1.0)
parser.add_argument('--max-samples', type=int, default=5000, help='Maximum samples taken from one genome if > 0')
parser.add_argument('--skip-genomes', type=str, nargs='+', default=[''])
parser.add_argument('--skip-datasets', type=str, nargs='+', default=[''], help='e.g. "gene_lengths"')
parser.add_argument('--dry-run', action='store_true', help='Just output what would be done')
args = parser.parse_args()
print(vars(args))

n_total_samples = 0
if not args.dry_run:
    h5_out = h5py.File(args.output_file, 'w')

need_to_create_datasets = True

for i, folder in enumerate(os.listdir(args.main_folder)):
    if folder.lower() in [g.lower() for g in args.skip_genomes]:
        print(f'skipping {folder}')
        continue
    start_time = time.time()
    h5_in = h5py.File(os.path.join(args.main_folder, folder, 'test_data.h5'), 'r')
    dsets_in = h5_in['data']

    n_samples_source = dsets_in['X'].shape[0]
    # have an exponent to undersample large genomes but also a linear coeffient to scale everything to where we want it
    n_samples = int(args.coefficient * math.pow(n_samples_source, args.exponent))
    n_samples = min(n_samples_source, n_samples)  # make sure there are enough samples
    if args.max_samples > 0:
        n_samples = min(args.max_samples, n_samples)
    n_total_samples += n_samples

    samples_idx = sorted(np.random.choice(n_samples_source, n_samples, replace=False))
    print(f'selecting {n_samples} samples of {folder}', flush=True)
    if not args.dry_run:
        for key in h5_in['data'].keys():
            if key not in args.skip_datasets:
                samples = dsets_in[key][samples_idx]
                if need_to_create_datasets:
                    HelixerExportController._create_dataset(h5_out, f'/data/{key}', samples, dsets_in[key].dtype)
                    dsets_out = h5_out['data']
                    need_to_create_datasets = False
                old_len = dsets_out[key].shape[0]
                dsets_out[key].resize(old_len + n_samples, axis=0)
                dsets_out[key][old_len:] = samples
    h5_in.close()
    print(f'added {n_samples} / {n_samples_source} samples of {folder} in {time.time() - start_time:.2f} secs', flush=True)

if not args.dry_run:
    h5_out.attrs['timestamp'] = str(datetime.datetime.now())
    for key, value in vars(args).items():
        h5_out.attrs[key] = value
    h5_out.close()

print(f'done, added {n_total_samples} to {args.output_file}')
