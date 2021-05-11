import sys
import getopt
import copy
import re
from BioHelpers.gffFastaTools import GFFParser


def make_id(n, prefix="Cc", depth=6):
    printer = "%0" + str(depth) + 'd'
    idfill = printer % int(n)
    newid = prefix + idfill
    return newid

def usage():
    print ("""
    ######################################
    #      make_unique_names.py  [AD]    #
    ######################################
    make gff with gene names replaced with continuously incrementing names. Assigns a new name every time
    it hits a feature == 'gene' entry; so sorting sensitive.

    usage:
        make_unique_names.py -g in.gff > out.gff
    options:
    -g in.gff, --gff=in.gff     input gff with your draft gene models
    -p prefix, --prefix=prefix  prefix species name (default Xx)
    -n N, --increment_from=N    start IDs from N (default 0)
    -h, --help                  prints this
      """)
    sys.exit(1)


def main():
    gffin = None
    prefix = "Xx"
    incrementing_id = 0
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "g:p:n:h", ["gff=", "prefix=", "increment_from=", "help"])
    except getopt.GetoptError as err:
        print (str(err))
        usage()
    for o, a in opts:
        if o in ("-g", "--gff"):
            gffin = a
        elif o in ("-p", "--prefix"):
            prefix = a
        elif o in ("-n", "--increment_from"):
            incrementing_id = int(a)
        elif o in ("-h", "--help"):
            usage()
        else:
            assert False, "unhandled option"

    if gffin is None:
        print("Input gff missing\n")
        usage()


    # read through gff file
    gff_r = GFFParser()

    for entry in gff_r.parse(gffin):
        if "gene" == entry._type:
            geneID = entry._attrib_dct['ID']
            incrementing_id += 1
        entry._attributes = re.sub(geneID, make_id(incrementing_id, prefix=prefix), entry._attributes)
        print(entry.toGFF3line())

if __name__ == "__main__":
    main()
