#! /usr/bin/env python3
import os
import time
import h5py
import argparse
import datetime
from helixer.export.exporter import HelixerExportController

parser = argparse.ArgumentParser()
parser.add_argument('--input-files', type=str, nargs='+', required=True)
parser.add_argument('--output-file', type=str, default='', required=True)
args = parser.parse_args()
print(vars(args))

n_files_added = 0
chunk_size = 10000
h5_out = h5py.File(args.output_file, 'w')
for input_path in args.input_files:
    start_time = time.time()
    h5_in = h5py.File(input_path, 'r')
    dsets_in = h5_in['data']

    n_samples = len(dsets_in['X'])
    for key in h5_in['data'].keys():
        samples = dsets_in[key][:chunk_size]
        if n_files_added == 0:
            HelixerExportController._create_dataset(h5_out, f'/data/{key}', samples, dsets_in[key].dtype)
            dsets_out = h5_out['data']

        # write out data in chunks to save memory
        old_len = len(dsets_out[key])
        dsets_out[key].resize(old_len + n_samples, axis=0)
        for offset in range(0, n_samples, chunk_size):
            print(f'{offset}/{n_samples}\r')
            samples = dsets_in[key][offset:offset + chunk_size]
            dsets_out[key][old_len + offset:old_len + offset + chunk_size] = samples
    h5_in.close()
    n_files_added += 1
    print(f'{n_files_added} / {len(args.input_files)} added {n_samples} samples of {input_path} '
          f'in {time.time() - start_time:.2f} secs', flush=True)

h5_out.attrs['timestamp'] = str(datetime.datetime.now())
for key, value in vars(args).items():
    h5_out.attrs[key] = value
h5_out.close()
