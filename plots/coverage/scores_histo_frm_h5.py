import numpy as np
import pandas as pd
import h5py
import argparse


# overall score
def score(f, other_y, n=20, by=1000):
    """get counts for histogram of reference scores broken up by other_y

    other_y should be a list of keys for h5 datasets to be compared to data/y, for each key
    this will record and return 8 histograms under the same key:
       [ig right, ig wrong, utr right, utr wrong, cds right, cds wrong, intron right, intron wrong]"""
    breaks = [x / n for x in range(n + 1)]
    histos = {}
    for key in other_y:
        histos[key] = [np.zeros((n,)) for _ in range(8)]

    for i in range(0, f['data/X'].shape[0], by):
        y = np.argmax(f['data/y'][i:(i + by)], axis=2).ravel()
        preds = {}
        for key in other_y:
            preds[key] = np.argmax(f[key][i:(i + by)], axis=2).ravel()
        scores = f['scores/by_bp'][i:(i + by)].ravel()

        for col in range(4):
            mask = y == col
            ysm = y[mask]
            scoressm = scores[mask]
            for key in other_y:
                predsm = preds[key][mask]
                maskright = (predsm == ysm).astype('bool')
                righthisto = np.histogram(scoressm[maskright], bins=breaks)[0]
                histos[key][col * 2] += righthisto
                histos[key][col * 2 + 1] += np.histogram(scoressm[np.logical_not(maskright)], bins=breaks)[0]
    index = []
    for cat in ['ig', 'utr', 'cds', 'exon']:
        index += [cat + '_agree', cat + '_disagree']

    pd_histos = {}
    for key in histos:
        pd_histos[key] = pd.DataFrame(histos[key])
        pd_histos[key].set_index(index)

    return pd_histos


def main(h5_data, alternatives, out_dir):
    f = h5py.File(h5_data, mode='r')
    other_y = ['predictions'] + ['alternative/' + x for x in alternatives.split(',')]
    pd_histos = score(f, other_y)

    for key in pd_histos:
        fkey = key.replace('/', '_')
        pd_histos[key].to_csv('{}/{}_scores.csv'.format(out_dir, fkey))

    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--h5-data', required=True,
                        help='h5 file with data/y, scores/by_bp dataset, [and alternative/*/y] datasets')
    parser.add_argument('-a', '--alternatives',
                        help='comma sep list of h5 groups where we will use alternative/{alternative}/y,'
                             ' e.g. "augustus"')
    parser.add_argument('-o', '--out-dir', default='./', help='directory where output will be written to')
    args = parser.parse_args()
    main(args.h5_data, args.alternative, args.out_dir)
