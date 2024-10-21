import argparse
import re
import copy

parser = argparse.ArgumentParser()
parser.add_argument('gff3')

args = parser.parse_args()

seen = set()

with open(args.gff3) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('#'):
            print(line)
        else:
            # clean up non-ID part of fasta headers
            sline = line.split('\t')
            sline[0] = re.sub(' .*', '', sline[0])
            # if it's the first mRNA for the gene, add gene
            # e.g.
            #NW_012130065.1  GeneMark.hmm3   mRNA    125     2660    .       +       .       ID=1_t;geneID=1_g
            # =>
            #NW_012130065.1  GeneMark.hmm3   gene    125     2660    .       +       .       ID=gene.1_g
            #NW_012130065.1  GeneMark.hmm3   mRNA    125     2660    .       +       .       ID=1_t;Parent=gene.1_g
            if sline[2] == "mRNA":
                _id = re.sub('.*geneID=', '', sline[8])
                _id = f'gene.{_id}'
                if _id not in seen:
                    seen.add(_id)
                    gline = copy.deepcopy(sline)
                    gline[2] = "gene"
                    gline[8] = f'ID={_id}'
                    print('\t'.join(gline))
                sline[8] = re.sub('geneID=.*', f'Parent={_id}', sline[8])
            # oh, and if it is a CDS, make a essentially duplicate line that is an exon as well
            elif sline[2] == "CDS":
                eline = copy.deepcopy(sline)
                eline[2] = 'exon'
                print('\t'.join(eline))


            print('\t'.join(sline))
