#! /usr/bin/env python3
import os
import time
import math
import h5py
import argparse
import numpy as np
import datetime
from multiprocess import Pool
from helixer.export.exporter import HelixerExportController

def sample_file(species, input_len):
    start_time = time.time()
    h5_in = h5py.File(os.path.join(args.main_folder, f'single_genomes_{input_len}k', species, 'test_data.h5'), 'r')
    h5_out = h5py.File(os.path.join(args.output_folder, f'{species}.h5'), 'w')
    dsets_in = h5_in['data']
    dsets_out = h5_out.create_group('data')

    n_samples_source = dsets_in['X'].shape[0]
    max_samples_adjusted = int(args.max_samples / (input_len / 20))  # take less sequences if input_len is longer
    n_samples = min(max_samples_adjusted, n_samples_source)

    samples_idx = sorted(np.random.choice(n_samples_source, n_samples, replace=False))
    print(f'selecting {n_samples} samples of {species} with length {input_len}', flush=True)
    for key in h5_in['data'].keys():
        if key not in args.skip_datasets:
            samples = dsets_in[key][samples_idx]
            HelixerExportController._create_dataset(h5_out, f'/data/{key}', samples, dsets_in[key].dtype)
            dsets_out[key].resize(n_samples, axis=0)
            dsets_out[key][:] = samples
    h5_in.close()

    h5_out.attrs['timestamp'] = str(datetime.datetime.now())
    for key, value in vars(args).items():
        h5_out.attrs[key] = value
    h5_out.close()
    print(f'added {n_samples} / {n_samples_source} samples of {species} in {time.time() - start_time:.2f} secs', flush=True)

parser = argparse.ArgumentParser()
parser.add_argument('--main-folder', type=str, default='', required=True,
                    help=('Main single genome folder. Expects "test_data.h5" files '
                          'inside "single_genomes_{20,50,100,200}k" subfolders.'))
parser.add_argument('--output-folder', type=str, default='', required=True)
parser.add_argument('--genome-length-file', type=str, default='animals_with_input_length',
                    help='CSV file that links genomes to their input length')
parser.add_argument('--max-samples', type=int, default=20000,
                    help='Maximum samples taken from one genome. Accounts for what would be taken at length 20k.')
parser.add_argument('--n-processes', type=int, default=8, help='May be useful due to compression even on single HDD machines.')
parser.add_argument('--skip-datasets', type=str, nargs='+', default=['gene_lengths'])
args = parser.parse_args()
print(vars(args))

os.makedirs(args.output_folder, exist_ok=True)

n_total_samples = 0
species, input_lens = [], []
for line in open(args.genome_length_file, 'r'):
    species.append(line.split(',')[0])
    input_lens.append(int(line.split(',')[1]))

with Pool(args.n_processes) as p:
    n_samples = p.starmap(sample_file, zip(species, input_lens))

print(f'done')
