#! /usr/bin/env python3
import h5py
import argparse
import datetime
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', type=str, default='', required=True)
parser.add_argument('--output-file', type=str, default='', required=True)
parser.add_argument('--remove-genomes', type=str, nargs='+', required=True)
parser.add_argument('--append', action='store_true')
args = parser.parse_args()
print(vars(args))

f = h5py.File(args.input_file, mode='r')
mode = 'a' if args.append else 'w'
newf = h5py.File(args.output_file, mode=mode)

# build mask for species we want to remove
species_names = np.array([s.decode().lower() for s in f['data/species'][:]])
mask = np.full(species_names.shape, True, dtype=np.bool)
for genome in args.remove_genomes:
    mask = np.logical_and(mask, species_names != genome.lower())
print(f'removing {np.sum(mask == False) / len(mask) * 100:.2f}% of samples')

for grp in f.keys():
    newf.create_group(grp)
    # setup datasets
    odat = f[grp]
    ndat = newf[grp]
    for key in odat.keys():
        shape = list(odat[key].shape)
        ndat.create_dataset(key,
                            shape=tuple([0] + shape[1:]),
                            maxshape=tuple([None] + shape[1:]),
                            chunks=tuple([1] + shape[1:]),
                            dtype=odat[key].dtype,
                            compression='lzf',
                            shuffle=odat[key].shuffle)
    by = 5000
    n_samples = f['data/y'].shape[0]
    for i in range(0, n_samples, by):
        print(f'{i}/{n_samples}', end='\r')
        submask = mask[i:(i + by)]
        n_seqs = np.sum(submask)
        if n_seqs > 0:
            old_end = ndat[list(ndat.keys())[0]].shape[0]

            for dset_key in odat.keys():
                # expand as necessary
                dset = ndat[dset_key]
                dset.resize(old_end + n_seqs, axis=0)

                # copy over
                dset[old_end:] = odat[dset_key][i:(i + by)][submask]
            newf.flush()

# copy over the metadata, start_end_i will be wrong, everything else should be OK
if 'meta' in newf.keys():
    newf.create_group('meta')
    for key in f['meta'].keys():

        bkey = key.encode('utf-8')
        h5py.h5o.copy(f['meta'].id, bkey, newf['meta'].id, bkey)

newf.attrs['timestamp-original-data'] = f.attrs['timestamp']
newf.attrs['timestamp-genome-removal'] = str(datetime.datetime.now())
newf.attrs['removed-genomes'] = args.remove_genomes
newf.close()
f.close()
