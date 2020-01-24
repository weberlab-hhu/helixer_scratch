import argparse
import sys


def main(input):
    i = 0
    with open(input) as f:
        for line in f:
            sline = line.split()  # splits at any white space... so hopefully mostly words
            for word in sline:
                try:
                    num = float(word)
                    print('found', num, file=sys.stderr)
                    i += 1
                except ValueError:
                    pass
    print('{}\ttotal floatable words'.format(i))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True,
                        help='Path to input text file')

    args = parser.parse_args()

    main(args.input)