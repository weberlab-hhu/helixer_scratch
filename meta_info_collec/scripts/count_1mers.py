#!/usr/bin/env python

import argparse

def main(filein):
    a, t, c, g, n = 0, 0, 0, 0, 0
    with open(filein) as f:
        for line in f:
            if not line.startswith('>'):
                line = line.lower()
                a += line.count("a")
                t += line.count("t")
                c += line.count("c")
                g += line.count("g")
                n += line.count('n')
    print("{}\t{}".format(a + t, 'A'))
    print("{}\t{}".format(c + g, 'C'))
    print("{}\t{}".format(n, 'N'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_fasta", 
            help="path to fasta file of DNA sequences")
    parser.parse_args()
    args = parser.parse_args()
    main(args.input_fasta)
