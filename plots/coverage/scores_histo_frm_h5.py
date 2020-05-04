import numpy as np
import pandas as pd
import h5py
import argparse
import itertools
import copy


# overall score
def score(f, other_y, predictions, n=1000, by=2000, max_bin=4):
    """get counts for histogram of normalized coverage broken up by other_y confusion matrix

    other_y should be a list of alternatives for y (ref or preds) as keys in the h5 file"""
    # double check our 'max_bin' is actually high enough to summarize data
    maxes_by_sp = f['meta/max_normalized_cov_sc'].attrs
    for sp in maxes_by_sp:
        assert max_bin > np.max(maxes_by_sp[sp])

    breaks = [x / n * max_bin for x in range(n + 1)]

    i_s = list(range(4))
    i_s_by_y = [i_s for _ in range(len(other_y))]
    argmax_sets = list(itertools.product(*i_s_by_y))

    histos = {}
    score_cats = ['cov', 'sc']
    for key in score_cats:
        histos[key] = [np.zeros((n,)) for _ in range(len(argmax_sets))]

    xshape = f['data/X'].shape[0]
    for i in range(0, xshape, by):
        print('at {} of {}'.format(i, xshape))
        un_padded = np.sum(f['data/X'][i:(i + by)], axis=2).ravel().astype(bool)
        preds = {}
        for key in other_y:
            of = f
            if key == 'predictions':
              of = predictions
            preds[key] = np.argmax(of[key][i:(i + by)], axis=2).ravel()[un_padded]
        scores = f['scores/norm_cov_by_bp'][i:(i + by)].reshape([-1, 2])[un_padded]

        for ih, argmaxes in enumerate(argmax_sets):
            subpreds = copy.deepcopy(preds)
            scoressm = copy.deepcopy(scores)

            # filter so that each "y" in other_y matches expected argmax
            for iam, am in enumerate((argmaxes)):
                mask = subpreds[other_y[iam]] == am
                for key in subpreds:
                    subpreds[key] = subpreds[key][mask]
                scoressm = scoressm[mask, :]

            for isc, sc_key in enumerate(score_cats):
                matchhisto = np.histogram(scoressm[:, isc], bins=breaks)[0]
                histos[sc_key][ih] += matchhisto

    pd_histos = {}
    for key in histos:
        pd_histos[key] = pd.DataFrame(histos[key])
        pd_histos[key].index = argmax_sets
        pd_histos[key].columns = breaks[:-1]

    return pd_histos


def main(h5_data, alternatives, out_dir, predictions):
    f = h5py.File(h5_data, mode='r')
    if predictions is None:
        pred_f = f
    else:
        pred_f = h5py.File(predictions, mode='r')
    other_y = ['data/y', 'predictions']
    other_y += ['alternative/{}/y'.format(x) for x in alternatives.split(',')]
    pd_histos = score(f, other_y, pred_f)

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
    parser.add_argument('-p', '--predictions', help='point to h5 with /predictions if not the same')
    args = parser.parse_args()
    main(args.h5_data, args.alternatives, args.out_dir, args.predictions)
