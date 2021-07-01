#! /usr/bin/env python3
import os
import h5py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--main-folder', type=str, default='', required=True)
args = parser.parse_args()

for folder in os.listdir(args.main_folder):
    f = h5py.File(os.path.join(args.main_folder, folder, 'test_data.h5'), 'r')
    if 'timestamp' in f.attrs:
        print(f'GOOD {folder}')
    else:
        print(f'BAD {folder}')
