#! /usr/bin/env python3

'''Checks if all .h5 files in the given folder have attributes, which means they
should have all the data'''

import glob
import os
import h5py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', type=str, required=True)
parser.add_argument('-sf', '--sub-folder', type=str, default='')
args = parser.parse_args()

for genome_folder in os.listdir(args.folder):
    if args.sub_folder == '':
        h5_files = glob.glob(os.path.join(args.folder, genome_folder, '*.h5'))
    else:
        h5_files = glob.glob(os.path.join(args.folder, genome_folder, args.sub_folder, '*.h5'))

    for h5_file in h5_files:
        try:
            f = h5py.File(h5_file, 'r')
        except OSError:
            print('ERROR', h5_file)
            continue

        if 'timestamp' in f.attrs:
            # the attributes should be written after all data has been saved
            print('OK', h5_file)
        else:
            print('ERROR', h5_file)
