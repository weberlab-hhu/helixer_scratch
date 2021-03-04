#! /usr/bin/env python3
"""Splits one input file into single genome h5 files. Useful for generating the larger generalization files to
be used after every training. Assumes all samples of one species are together."""

import os
import time
import h5py
import argparse
import datetime
import numpy as np
from helixer.export.exporter import HelixerExportController

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', type=str, default='', required=True)
parser.add_argument('--output-folder', type=str, default='./genomes')
args = parser.parse_args()
print(vars(args))

if not os.path.isdir(args.output_folder):
    os.makedirs(args.output_folder)
    print(f'{args.output_folder} generated')
h5_in = h5py.File(args.input_file, 'r')

# find transition points in species array
species = h5_in['data/species'][:]
species_padded = np.insert(species, 0, species[0])
transitions = np.where(species_padded[:-1] != species_padded[1:])[0]

# add start and end to conveniently construct slices
transitions = np.insert(transitions, 0, 0)
transitions = np.insert(transitions, len(transitions), len(species))

for i in range(len(transitions) - 1):
    species_slice = slice(transitions[i], transitions[i + 1])
    species_name = species[species_slice.start].decode()
    print(f'starting with {species_name} ({species_slice.start}-{species_slice.stop})')

    h5_out = h5py.File(os.path.join(args.output_folder, f'{species_name}.h5'), 'w')
    for key in h5_in['data'].keys():
        data = h5_in['data'][key][species_slice]
        HelixerExportController._create_dataset(h5_out, f'/data/{key}', data, data.dtype)
        h5_out['data'][key].resize(len(data), axis=0)
        h5_out['data'][key][:] = data

    h5_out.attrs['timestamp-split'] = str(datetime.datetime.now())
    h5_out.attrs['split-input-file'] = args.input_file
    for key, value in h5_in.attrs.items():
        h5_out.attrs[key] = value
    h5_out.close()
h5_in.close()
