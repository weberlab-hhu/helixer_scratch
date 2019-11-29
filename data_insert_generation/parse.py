#! /usr/bin/env python3

data = [['genome', 'percent_intergenic', 'percent_error']]
genome = []
for line in open('all_genomes_generation_output_truncated'):
    if line.startswith('/home/'):
        genome.append(line.split('/')[6])
    elif line.startswith('Total intergenic'):
        genome.append('{:.4f}'.format(float(line.split(' ')[2].split('%')[0]) / 100))
    elif line.startswith('Total errors'):
        genome.append('{:.4f}'.format(float(line.split(' ')[2].split('%')[0]) / 100))
        data.append(genome)
        genome = []

for genome in data:
    print('\t'.join(genome))


