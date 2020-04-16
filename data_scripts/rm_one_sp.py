import h5py
import numpy as np

f = h5py.File('training_data.h5', mode='r')
newf = h5py.File('training_with_coverage.h5', mode='a')

# we want to remove Mguttatus bc we have no stranded RNAseq data for it
mask = f['data']['species'][:] != b'Mguttatus'

#for grp in ['evaluation', 'scores']:
for grp in ['scores', 'data', 'evaluation']:    
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
    by = 500
    for i in range(0, f['data/y'].shape[0], by):
        submask = mask[i:(i + by)]
        n_seqs = np.sum(submask)
        old_end = ndat[list(ndat.keys())[0]].shape[0]

        for dset_key in odat.keys():
            # expand as necessary
            dset = ndat[dset_key]
            dset.resize(old_end + n_seqs, axis=0)

            # copy over
            dset[old_end:] = odat[dset_key][i:(i + by)][submask]
    newf.flush()

# copy over the metadata, start_end_i will be wrong, everything else should be OK
newf.create_group('meta')
for key in f['meta'].keys():

    bkey = key.encode('utf-8')
    h5py.h5o.copy(f['meta'].id, bkey, newf['meta'].id, bkey)

newf.close()
f.close()
