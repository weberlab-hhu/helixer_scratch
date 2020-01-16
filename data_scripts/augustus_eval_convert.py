#! /usr/bin/env python3

# reads the raw confusion matrix of agustus evals into ConfusionMatrix
# and outputs the metric tables

import os
import argparse
from helixerprep.prediction.ConfusionMatrix import ConfusionMatrix

parser = argparse.ArgumentParser()
parser.add_argument('folder', type=str)
args = parser.parse_args()

cm = ConfusionMatrix(None)
csv_cm_file = os.path.join(args.folder, 'confusion_matrix.csv')
if os.path.exists(csv_cm_file):
    for i, line in enumerate(open(csv_cm_file)):
        if i > 0:
            parts = line.strip().split(',')
            cm.cm[i - 1] = parts[1:]
    cm.print_cm()
