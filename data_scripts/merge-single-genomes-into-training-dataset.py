#! /usr/bin/env python3
import os
import time
import h5py
import argparse
import datetime
from helixer.export.exporter import HelixerExportController

parser = argparse.ArgumentParser()
parser.add_argument('--main-folder', type=str, default='', required=True,
                    help='Main single genome folder. Expects "test_data.h5" files inside subfolders.')
parser.add_argument('--output-file', type=str, default='./training_data.h5')
parser.add_argument('--genomes', type=str, nargs='+', required=True)
args = parser.parse_args()
args.genomes = [g.lower() for g in args.genomes]
print(vars(args))

n_genomes_added = 0
h5_out = h5py.File(args.output_file, 'w')
for folder in os.listdir(args.main_folder):
    start_time = time.time()
    if folder.lower() in args.genomes:
        h5_in = h5py.File(os.path.join(args.main_folder, folder, 'test_data.h5'), 'r')
        dsets_in = h5_in['data']

        for key in h5_in['data'].keys():
            samples = dsets_in[key][:]
            n_samples = len(samples)
            if n_genomes_added == 0:
                HelixerExportController._create_dataset(h5_out, f'/data/{key}', samples, dsets_in[key].dtype)
                dsets_out = h5_out['data']
            old_len = dsets_out[key].shape[0]
            dsets_out[key].resize(old_len + n_samples, axis=0)
            dsets_out[key][old_len:] = samples
        h5_in.close()
        n_genomes_added += 1
        print(f'{n_genomes_added} / {len(args.genomes)} added {n_samples} samples of {folder} '
              f'in {time.time() - start_time:.2f} secs', flush=True)

h5_out.attrs['timestamp'] = str(datetime.datetime.now())
for key, value in vars(args).items():
    h5_out.attrs[key] = value
h5_out.close()
