### previous bug caused the coverage based scoring to use normalization from pooled species instead
### of from each species. While patched for the future, this scripts helps rerun just that which
### is necessary (i.e. saves a day of wait & CPU time)


import argparse
import h5py
from helixer.evaluation.training_rnaseq import get_median_expected_coverage


def main(h5_data):
    f = h5py.File(h5_data, 'a')
    
    for species in f['meta/start_end_i'].attrs.keys():
        fixed_mec = get_median_expected_coverage(f, species)
        old_mec = f['meta/median_expected_coverage'].attrs[species]
        f['meta/median_expected_coverage'].attrs[species] = fixed_mec
        print(f'fixed {species}, was {old_mec}, now {fixed_mec}')

    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('h5_data', help='h5 data file, which already has coverage, but still has buggy median expected coverage, and therefore scores; file will be fixed in place')
    args = parser.parse_args()
    main(args.h5_data)
