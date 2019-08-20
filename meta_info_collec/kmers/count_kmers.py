#!/usr/bin/env python
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from kpal.klib import Profile

def count_seq(seq, k):
    prof = Profile.from_sequences(sequences=[seq], length=k)
    kmers = [prof.binary_to_dna(x) for x in range(len(prof.counts))]
    return prof.counts, kmers


def main(fastain, min_k, max_k):
    print('\t'.join(["coordinate_id", "mer_sequence", "count", "length"]))
    for record in SeqIO.parse(fastain, format="fasta"):
        seq = str(record.seq).upper()
        for k in range(min_k, max_k + 1, 1):
            counts, kmers = count_seq(seq, k)
            count_dict = dict()
            for count, kmer in zip(counts, kmers):
                count_dict[str(kmer)] = int(count)
            # collapse to canonical kmers
            to_del = []
            for kmer in count_dict:
                kmer_rc = str(Seq(kmer, generic_dna).reverse_complement())
                if kmer > kmer_rc:
                    count_dict[kmer_rc] += count_dict[kmer]
                    to_del.append(kmer)
            for kmer in to_del:
                count_dict.pop(kmer)
            for kmer in sorted(count_dict):
                count = count_dict[kmer]
                print('\t'.join([str(x) for x in [record.id, kmer, count, k]]))
        print('\t'.join([str(x) for x in [record.id, 'N', seq.count('N'), 1]]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_fasta",
            help="path to fasta file of DNA sequences")
    parser.add_argument("--min_k", default=1, type=int, help="smallest k for kmers to count")
    parser.add_argument("--max_k", default=3, type=int, help="largest k for kmers to count")

    args = parser.parse_args()
    main(args.input_fasta, args.min_k, args.max_k)

