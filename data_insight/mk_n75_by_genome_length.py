#! /usr/bin/env python3

# reads in a metadata csv file and outputs a csv with just two columns: species,n75/genome_length

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--metadata_file', type=str, default='../metadata_csvs/plant_metadata.csv')
parser.add_argument('--output_file', type=str, default='output.csv')
parser.add_argument('--sort-by', type=str, default='N75/total_len')
args = parser.parse_args()

df = pd.read_csv(args.metadata_file)
df['N75/total_len'] = df['N75'] / df['total_len']
df = df.sort_values(args.sort_by, ascending=False)
df.to_csv(args.output_file, columns=['species', 'N75', 'total_len', 'N75/total_len'], index=False)
print(f'{args.output_file} written')
