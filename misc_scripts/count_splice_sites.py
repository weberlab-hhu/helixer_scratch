import click
import itertools
import sys


def gen_seqs_from_fasta(fasta):
    seqid = None
    seq = ''
    with open(fasta) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('>'):
                if seqid is not None:
                    yield seqid, seq
                    seq = ''
                seqid = line.split()[0][1:]  # until the space, and drop the '>'
            else:
                line = line.upper()
                line = line.replace('U', 'T')
                seq += line
    yield seqid, seq


@click.command()
@click.argument('introns_fasta')
@click.option('-o', '--file-out', help='output file, defaults to stdout')
def main(introns_fasta, file_out):
    two_mers = [''.join(x) for x in itertools.product('ACTG', repeat=2)]
    pairs = itertools.product(two_mers, two_mers)
    sites = {mer_pair: 0 for mer_pair in pairs}
    sites[('NN', 'NN')] = 0
    sites['too_short'] = 0
    for _, seq in gen_seqs_from_fasta(introns_fasta):
        try:
            sites[(seq[:2], seq[-2:])] += 1
        except KeyError:
            print(f'key error for {(seq[:2], seq[-2:])}, adding to err category', file=sys.stderr)
            if len(seq[:2]) == len(seq[-2:]) == 2:  # probably ambiguous, make fully so
                sites[('NN', 'NN')] += 1
            else:
                sites['too_short'] += 1
    if file_out is None:
        f = sys.stdout
    else:
        f = open(file_out, 'w')
    print('donor_acceptor\tcount', file=f)
    for mer, count in sites.items():
        print(f'{mer}\t{count}', file=f)
    f.close()


if __name__ == "__main__":
    main()
