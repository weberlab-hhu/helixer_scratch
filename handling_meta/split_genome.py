from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import argparse


def start_ends(length, max_chunk):
    edges = iter(range(0, length, max_chunk))
    start = next(edges)
    for end in edges:
        yield start, end
        start = end
    if start != length:
        yield start, length
#fain = 'train/Athaliana/TAIR10/assembly/Athaliana_167_TAIR9.fa'
#faout = 'tmp/Athaliana_split.fa'


def main(fain, faout, chunk_size):
    out = []
    for record in SeqIO.parse(fain, 'fasta'):
        for start, end in start_ends(len(record.seq), chunk_size):
            seq = record.seq[start:end]
            sr = SeqRecord(seq,
                           id='{}:{}-{}'.format(record.id, start, end))
            out.append(sr)

    with open(faout, 'w') as f:
        SeqIO.write(out, f, 'fasta')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--fasta_in', help="input fasta file to split")
    parser.add_argument('-o', '--fasta_out', help="output split up fasta file")
    parser.add_argument('--chunk_size', default=20000, help="size of chunks to split fasta into", type=int)
    args = parser.parse_args()
    main(args.fasta_in, args.fasta_out, args.chunk_size)