#! /usr/bin/env python

import click
from dustdas import gffhelper

def gff_gen(gff_file):
    reader = gffhelper.read_gff_file(gff_file)
    for entry in reader:
        clean_entry(entry)
        yield entry

def clean_entry(entry):
    # always present and integers
    entry.start = int(entry.start)
    entry.end = int(entry.end)


def str_entry(entry):
    out = [entry.seqid,
           entry.source,
           entry.type,
           entry.start,
           entry.end,
           entry.score,
           entry.strand,
           entry.phase,
           entry.attribute]
    return "\t".join([str(c) for c in out])


def cds_length(entries):
    l = 0
    for entry in entries:
        if entry.type == "CDS":
            l += entry.end - entry.start + 1
    return l

@click.command()
@click.option("-i", "--gff-file", required=True)
def main(gff_file):
    transcripts = {}
    for entry in gff_gen(gff_file):
        if entry.type in ["gene", "pseudogene"]:
            if transcripts:
                longest = max(transcripts.values(), key=lambda x: cds_length(x))
                print(str_entry(gene_entry))
                for e in longest:
                    print(str_entry(e))
            transcripts = {}
            gene_id = entry.get_ID()
            gene_entry = entry
        elif entry.type in ['mRNA', 'transcript']:
            assert entry.get_Parent()[0] == gene_id, f"{entry.get_Parent()[0]} != {gene_id}"
            transcript_id = entry.get_ID()
            transcripts[transcript_id] = [entry]
        elif entry.type in ['exon', 'CDS']:
            # assumes sorted order, checking would be safer
            
            # this throws when a gene didn't have an mRNA/transcript feature
            # but skipped straight to exon/CDS
            # will just skip to the next gene
            # it's mostly because tRNA...
            try:
                transcripts[transcript_id].append(entry)
            except KeyError:
                continue

if __name__ == "__main__":
    main()
