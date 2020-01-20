#! /usr/bin/env python3

'''Checks if all .h5 files in the given folder have attributes, which means they
should have all the data'''

import glob
import os
import h5py
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('folder', type=str)
parser.add_argument('-sf', '--sub-folder', type=str, default='')
parser.add_argument('-del', '--delete', action='store_true', help='Remove folders with errors')
args = parser.parse_args()

for genome_folder in os.listdir(args.folder):
    folder = os.path.join(args.folder, genome_folder)
    if os.path.isdir(folder):
        if args.sub_folder == '':
            h5_files = glob.glob(os.path.join(folder, '*.h5'))
        else:
            h5_files = glob.glob(os.path.join(folder, args.sub_folder, '*.h5'))

        # switch whether to delete the whole folder if --delete is set
        # also deletes if dir does not contain h5 files
        found_only_errors = True
        for h5_file in h5_files:
            try:
                f = h5py.File(h5_file, 'r')
            except OSError:
                print('ERROR', h5_file)
                continue

            if 'timestamp' in f.attrs:
                # the attributes should be written after all data has been saved
                print('OK', h5_file)
                found_only_errors = False # one good file stops the folder purge
            else:
                print('ERROR', h5_file)

        if args.delete and found_only_errors:
            shutil.rmtree(folder)
            print(folder, 'deleted')
