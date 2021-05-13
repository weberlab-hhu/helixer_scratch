__author__ = 'adenton'

from dustdas import fastahelper
import argparse


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
    if cumulative_char >= nchar != -1:
        out = True
    return out


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input fasta file', required=True)
    parser.add_argument('-o', '--output', help='output prefix (default = conform_fasta_out)',
                        default="conform_fasta_out")

    parser.add_argument('-l', '--length', help='characters per line in sequence', type=int, default=60)
    parser.add_argument('-n', '--nseqs', help='split into subfiles with maximum of N sequences each', default=-1,
                        type=int)
    parser.add_argument('-c', '--nchar', help='split into subfiles with maximum of N characters (bases) each',
                        default=-1, type=int)
    parser.add_argument('-m', '--min-length', type=int, help='drop all sequences shorter than m')
    parser.add_argument('-x', '--max-length', type=int, help='drop all sequences longer than x')
    parser.add_argument('-d', '--id-delimiter', help='delimiter of id')
    parser.add_argument('-p', '--id-pieces', help='comma separated pieces (indexes from 0) of id to keep')
    parser.add_argument('-u', '--unique-ids', help='add ever increasing numbers for force IDs to be unique '
                                                   '(only set if they are not)', action='store_true')

    args = parser.parse_args()
    filein = args.input
    new_length = args.length
    nseqs = args.nseqs
    nchar = args.nchar
    pfxout = args.output
    max_length = args.max_length
    min_length = args.min_length
    id_delimiter = args.id_delimiter
    id_pieces = args.id_pieces
    unique_ids = args.unique_ids

    fastaparser = fastahelper.FastaParser()

    # write to separate files only if nseqs or nchar has been set
    if nseqs == -1 and nchar == -1:
        mid_file = ''
    elif nseqs != -1 and nchar != -1:
        raise ValueError("Options -c and -n are incompatible. Choose one of them.")
    else:
        nfile = 0
        mid_file = '{:03}'.format(nfile)

    uniquifier = 0
    counter = 0
    cumulative_char = 0
    fileout = pfxout + mid_file + '.fa'
    openout = open(fileout, 'w')
    file_is_still_empty = True  # keep from writing empty file 00
    for seq in fastaparser.read_fasta(filein):
        if length_ok(len(seq[1]), max_length=max_length, min_length=min_length):
            cumulative_char += len(seq[1])
            if counter == nseqs or reached_nchar(cumulative_char, nchar) and not file_is_still_empty:
                openout.close()
                nfile += 1
                counter = 0
                cumulative_char = 0
                fileout = '{}{:03}.fa'.format(pfxout, nfile)
                openout = open(fileout, 'w')

            oldid = id_fix(seq[0], id_delimiter=id_delimiter, id_pieces=id_pieces)
            if unique_ids:
                oldid = make_unique(oldid, uniquifier)  # todo, pass delimiter if set from id_delimiter
            openout.write('>' + oldid + '\n')
            for substring in chunkstring(seq[1], new_length):
                openout.write(substring + '\n')
            file_is_still_empty = False
        counter += 1
        uniquifier += 1


if __name__ == "__main__":
    main()
