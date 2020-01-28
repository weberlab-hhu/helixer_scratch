import argparse
import copy


def main(filein, fileout):
    handleout = open(fileout, 'w')
    with open(filein) as f:
        for line in f:
            line = line.rstrip()
            sline = line.split('\t')
            # insert exons for every CDS
            if line.startswith('#'):
                pass  # just copy over comment lines without further parsing
            elif sline[2] == "CDS":
                exonsline = copy.deepcopy(sline)
                # change feature type
                exonsline[2] = "exon"
                # unique (exon) ID
                exonsline[8] = exonsline[8].replace('cds', 'exon')
                handleout.write('\t'.join(exonsline) + '\n')
            # change transcript features to mRNA (bc idk why they're called transcript and have CDS here)
            elif sline[2] == "transcript":
                sline[2] = 'mRNA'
            handleout.write('\t'.join(sline) + '\n')
    handleout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--gff_in', help='input gff3, produced from augustus called with --gff3=on --UTR=off',
                        required=True)
    parser.add_argument('-o', '--out', help='output gff3 filename', required=True)
    args = parser.parse_args()
    main(args.gff_in, args.out)