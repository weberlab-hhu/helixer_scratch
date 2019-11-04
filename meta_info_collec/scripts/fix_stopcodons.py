import sys
import argparse

def main(args):
    if args.out is None:
        fileout = sys.stdout
    else:
        fileout = open(args.out, "w")

    with open(args.input, "r") as f:
        for line in f:
            line=line.rstrip()
            if not line.startswith('>'):
                line = line.replace(args.find, args.replace)
            print(line, file=fileout)
    fileout.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()


    parser.add_argument('-i', '--input', help='fa file with wrong stop codons', required=True)
    parser.add_argument('-o', '--out', help='output file name (default stdout)')
    parser.add_argument('--find', help='old stop codon to be replace (default ".")', default=".")
    parser.add_argument('--replace', help='stop codon to replace with (default "*"', default="*")

    a = parser.parse_args()
    main(a)
