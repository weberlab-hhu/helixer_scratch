#! /usr/bin/env python3
import os
import math
import h5py
import argparse
import numpy as np
import datetime
from helixer.export.exporter import _create_dataset

parser = argparse.ArgumentParser()
parser.add_argument('--main-folder', type=str, default='', required=True,
                    help='Main single genome folder. Expects "test_data.h5" files inside subfolders.')
parser.add_argument('--output-file', type=str, default='./generalization_validation.h5')
args = parser.parse_args()

h5_out = h5py.File(args.output_file, 'w')
for i, folder in enumerate(os.listdir):
    h5_single = h5py.File(os.path.join(args.main_folder, folder), 'r')
    dsets = h5_single['data']

    # sample sqrt(n_samples) from each genome
    n_samples_source = dsets['X'].shape[0]
    n_samples = math.sqrt(n_samples_source)
    samples_idx = sorted(np.random.choice(n_samples_source, n_samples, replace=False))
    for key  in h5_single['data'].keys():
        samples = dsets[key][samples_idx]
        if i == 0:
            _create_dataset(h5_out, key, samples, dsets[key].dtype)
        else:
            old_len = dsets[key].shape[0]
            dsets[key].resize(old_len + n_samples, axis=0)
        dsets[key][old_len:] = samples
    h5_single.close()
    print(f'added {n_samples} of {folder}')

h5_out.attrs['timestamp'] = datetime.datetime.now()
h5_out.close()
