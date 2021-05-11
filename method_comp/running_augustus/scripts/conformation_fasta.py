__author__ = 'adenton'
import sys
import getopt
import fastahelper

def usage():
    usagestr = """ python conformation_fasta.py -i sequences.fasta -o ouput.fasta[options]
###############
-i | --in=              input fasta file
-o | --out=             output prefix (default = conform_fasta_out)
-l | --length=   	    desired line length (default = 60)
-n | --nseqs=           split output in subfiles with n sequences (incompatible with -c)
-c | --nchar=           split output into new file whenever c characters is reached (incompatible with -n)
-m | --min-length=      drop all sequences shorter than m
-x | --max-length=      drop all sequences longer than x
-d | --id_delimiter=    delimiter of id
-p | --id_pieces=       comma separated pieces (indexes from 0) of id to keep
-u | --unique_ids=      add ever increasing numbers for force IDs to be unique (only set if they aren't)
-h | --help             prints this message
"""
    print(usagestr)
    sys.exit(1)


def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


def make_unique(string, number, delim='|'):
    out = string + str(delim) + str(number).zfill(7)
    return out


def id_fix(my_id, id_delimiter=None, id_pieces=None):
    if id_delimiter is not None and id_pieces is not None:
        id_pieces = [int(x) for x in id_pieces]
        if id_delimiter is None or id_pieces is None:
            keep_id = my_id
        else:
            list_id = my_id.split(id_delimiter)
            keep_id = []
            for id_piece in id_pieces:
                keep_id += [list_id[id_piece]]
        keep_id = id_delimiter.join(keep_id)
    elif id_delimiter is not None or id_pieces is not None:
        raise ValueError("IDs can only be modified if both 'id_delimiter' and 'id_pieces' are specified")
    else:
        keep_id = my_id
    return keep_id


def length_ok(length, max_length, min_length):
    """
    checks that length is between min_length and max_length if the latter two are defined
    :param length:
    :param max_length:
    :param min_length:
    :return: True if between or limit not set, else False
    """
    out = True
    if max_length is not None:
        if length > max_length:
            out = False
    if min_length is not None:
        if length < min_length:
            out = False
    return out


def reached_nchar(cumulative_char, nchar):
    """
    checks whether cumulative_char greater than nchar if nchar isn't -1
    :param cumulative_char: int
    :param nchar: int
    :return: boolean
    """
    out = False
    if cumulative_char >= nchar and nchar != -1:
        out = True
    return out


def main():
    filein = None
    new_length = 60
    nseqs = -1
    pfxout = "conform_fasta_out"
    max_length = None
    min_length = None
    id_delimiter = None
    id_pieces = None
    nchar = -1
    unique_ids = False
    # get opt
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "i:l:n:c:m:x:d:p:o:uh",
                                       ["in=", "length=", "nseqs=", "nchar=", "min-length=", "max-length=", "id_delimiter=",
                                        "id_pieces=", "out=", "unique_ids", "help"])
    except getopt.GetoptError as err:
        print (str(err))
        usage()

    for o, a in opts:
        if o in ("-i", "--in"):
            filein = a
        elif o in ("-l", "--length"):
            new_length = int(a)
        elif o in ("-n", "--nseqs"):
            nseqs = int(a)
        elif o in ("-c", "--nchar"):
            nchar = int(a)
        elif o in ("-m", "--min-length"):
            min_length = int(a)
        elif o in ("-x", "--max-length"):
            max_length = int(a)
        elif o in ("-d", "--id_delimiter"):
            id_delimiter = a
        elif o in ("-p", "--id_pieces"):
            id_pieces = a.split(',')
        elif o in ("-o", "--out"):
            pfxout = a
        elif o in ("-u", "--unique_ids"):
            unique_ids = True
        elif o in ("-h", "--help"):
            usage()
        else:
            assert False, "unhandled option"
    
    if filein is None:
        print("input fasta required")
        usage()
    # todo, check set both or none -d -p
    fastaparser = fastahelper.FastaParser()

    # write to separate files only if nseqs has been set
    if nseqs == -1 and nchar == -1:
        nfile = ''
    elif nseqs != -1 and nchar != -1:
        print("Options -c and -n are incompatible. Choose one of them.")
        usage()
    else:
        nfile = 0

    uniquifier = 0
    counter = 0
    cumulative_char = 0
    fileout = pfxout + str(nfile) + '.fa'
    openout = open(fileout, 'w')
    for seq in fastaparser.read_fasta(filein):
        if length_ok(len(seq[1]), max_length=max_length, min_length=min_length):
            cumulative_char += len(seq[1])
            if counter == nseqs or reached_nchar(cumulative_char, nchar):
                openout.close()
                nfile += 1
                counter = 0
                cumulative_char = 0
                fileout = pfxout + str(nfile) + '.fa'
                openout = open(fileout, 'w')

            oldid = id_fix(seq[0], id_delimiter=id_delimiter, id_pieces=id_pieces)
            if unique_ids:
                oldid = make_unique(oldid, uniquifier)  # todo, pass delimiter if set from id_delimiter
            openout.write('>' + oldid + '\n')
            for substring in chunkstring(seq[1], new_length):
                openout.write(substring + '\n')
        counter += 1
        uniquifier += 1
if __name__ == "__main__":
    main()
