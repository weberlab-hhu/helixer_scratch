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
parser.add_argument('--data-file', type=str, default='', required=True)
parser.add_argument('--prediction-file', type=str, nargs='+', required=True)
args = parser.parse_args()
print(vars(args))
n_preds = len(args.prediction_file)
chunk_size = 10000

h5_data = h5py.File(args.data_file, 'r')
shape = h5_data['/data/X'].shape
shape = (0,) + shape  # additional dimension for the individual predictions
h5_data.create_dataset('/data/predictions',
                       shape=shape,
                       maxshape=(None,) + shape[1:],
                       chunks=(n_preds, 1) + shape[2:]),
                       dtype='float16',
                       compression='lzf',
                       shuffle=True)
dest = h5_data['/data/predictions']
for i, pred_file in enumerate(args.prediction_file):
    start_time = time.time()
    h5_pred = h5py.File(pred_file, 'r')
    source = h5_pred['predictions']

    dest.resize(i + 1, axis=0)
    for offset in range(0, shape[1], chunk_size):
        dest[i, offset:offset + chunk_size] = source[offset:offset + chunk_size]
    source.close()
    print(f'{i + 1} / {n_preds} added samples of {pred_file} in {time.time() - start_time:.2f} secs', flush=True)

h5_data.attrs['prediction_files'] = prediction_file
h5_data.close()
