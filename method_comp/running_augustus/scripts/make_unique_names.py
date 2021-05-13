"""restore unique naming scheme for gene models if, e.g., sequences were ran through the predictor individually,
instead of as a whole genome, and current gene IDs are non-unique. Also adds species prefix. Assumes all transcript
names etc exactly contain the gene ID; if this isn't true Transcript IDs won't end up unique.
It works for AUGUSTUS output"""

import re
import argparse
from dustdas import gffhelper


def make_id(n, prefix="Cc", depth=6):
    printer = "%0" + str(depth) + 'd'
    idfill = printer % int(n)
    newid = prefix + idfill
    return newid


def dump2gffline(entry):
    return '\t'.join([str(x) for x in [entry.seqid, entry.source, entry.type, entry.start, entry.end, entry.score,
                                       entry.strand, entry.phase, entry.attribute]])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gff', help='input gff with our draft gene models', required=True)
    parser.add_argument('-p', '--prefix', help='prefix species name (default Xx)', default='Xx')
    parser.add_argument('-n', '--increment-from', help='start IDs counting from N', default=0, type=int)
    args = parser.parse_args()
    gffin = args.gff
    prefix = args.prefix
    incrementing_id = args.increment_from

    # read through gff file
    reader = gffhelper.read_gff_file(gffin)

    for entry in reader:
        if "gene" == entry.type:
            geneID = entry.get_ID()
            incrementing_id += 1
        entry.attribute = re.sub(geneID, make_id(incrementing_id, prefix=prefix), entry.attribute)
        print(dump2gffline(entry))


if __name__ == "__main__":
    main()
