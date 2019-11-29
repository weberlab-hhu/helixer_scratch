import sys

digits = [str(x) for x in range(10)]


def parse_cigar(cigar):
    if cigar == "*":
        return
    n = ''
    for char in cigar:
        if char in digits:
            n += char
        else:
            try:
                yield int(n), char
            except ValueError as e:
                print('cigar', cigar)
                raise e
            n = ''


with sys.stdin as f:
    for line in f:
        line = line.rstrip()
        sline = line.split()
        for n, key in parse_cigar(sline[5]):
            if key  in ["N", "D"]:
                print('{},{}'.format(n, key))
