import re 
import click
import sys

# borrowed and modified from dustdas
def get_attr_val_by_tag(line, tag):
    attr = line.split()[8]
    p = re.compile(r"""(.*)=(.*)""")
    for tag_val in attr.split(';'):
        m = p.match(tag_val)
        if m:
            if m.groups()[0] == tag:
                return m.groups()[1]
    return None


@click.command()
@click.option('-i', '--input-gff3', required=True)
@click.option('-o', '--output-gff3', help='output file, default (stdout)')
def main(input_gff3, output_gff3):
    """filters lines from gff3 file where parent is expected but hasn't been seen (e.g. orphaned exons)"""
    seen = {None}

    if output_gff3 is None:
        of = sys.stdout
    else:
        of = open(output_gff3, 'w')

    with open(input_gff3) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('#'):
                print(line, file=of)
                continue
            lid = get_attr_val_by_tag(line, 'ID')
            seen.add(lid)
            lparent = get_attr_val_by_tag(line, 'Parent')
            if lparent in seen:  # top level w/o parent has a parent of None, which is in seen; every thing else subject to filtering
                print(line, file=of)


if __name__ == "__main__":
    main()
