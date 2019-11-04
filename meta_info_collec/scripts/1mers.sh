#!/bin/bash
basedir=$1
sp=$2
fasta_in=`echo $basedir/$sp/*/assembly/*.fa`
outdir=$basedir/$sp/meta_collection/jellyfish

mkdir -p $outdir
python $metapath/scripts/count_1mers.py $fasta_in > $outdir/k1mer_counts.tsv
