import numpy as np


def count(f, training_genomes):
    values = []
    for i, line in enumerate(open(f)):
        if i > 1 and (not training_genomes or line.strip().split()[0] in training_genomes):
            values.append(int(line.strip().split()[2]))
    print('median', np.median(values))
    print('mean', np.mean(values))
    print('std', np.std(values))
