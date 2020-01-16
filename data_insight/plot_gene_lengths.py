#! /usr/bin/env python3

# plots histograms of the gene lengths and the loss impact of each bin
# for each genome in the given "gene_lengths" file which is expected to have 4 columns

import argparse
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=str)
args = parser.parse_args()

genome_values = defaultdict(list)
for i, line in enumerate(open(args.input_file)):
    if i > 1:
        parts = [e for e in line.strip().split(" ") if len(e) > 0]
        genome, value = parts[0], int(parts[2])
        if value <= 100000:
            genome_values[genome].append(value)

for genome, values in genome_values.items():
    # plot normal gene length plot
    plt.clf()
    plt.title(genome)
    plt.hist(values, bins=200)
    plt.savefig(f'{genome}_lengths.png')
    print(f'saved {genome}_lengths.png')

    # plot loss influence graph per bin
    bin_values, bin_edges = np.histogram(values, bins=200)
    plt.clf()
    plt.title(genome)
    plt.plot(bin_values * bin_edges[1:])
    plt.savefig(f'{genome}_bin_weights.png')
    print(f'saved {genome}_bin_weights.png')
