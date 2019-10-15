import os
import argparse
import subprocess


def to_checksum_dict(path):
    out = {}
    with open(path + 'CHECKSUMS', 'r') as f:
        for line in f:
            line = line.rstrip()
            sline = line.split()
            out[sline[-1]] = sline[:-1]
    return out


def check_dir(path):
    if not path.endswith('/'):
        path = path + '/'

    checksums = to_checksum_dict(path)

    files = os.listdir(path)
    files = [x for x in files if x != 'CHECKSUMS']
    for fil in files:
        cs = subprocess.check_output(['sum', path + fil])
        cs = cs.decode('utf-8')
        cs = cs.rstrip()
        cs = cs.split()
        if checksums[fil] != cs:
            print("FAIL {} != {} @ {}".format(checksums[fil], cs, path + fil))
        else:
            print('successfully checked {}'.format(path + fil))


def main(basedir, subdir):
    for root, dirs, files in os.walk(basedir, topdown=False):
        if root.endswith(subdir):
            check_dir(root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help="will recursively search for subdirectories with in this directory",
                        required=True)
    parser.add_argument('-s', '--sub_dir', help='target directories containing CHECKSUMS file and files to check',
                        required=True)
    args = parser.parse_args()
    main(args.dir, args.sub_dir)
