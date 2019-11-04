#!/bin/bash
basedir=$1
sp=$2
fasta_in=`echo $basedir/$sp/*/assembly/*.fa`
outdir=$basedir/$sp/meta_collection/jellyfish

mkdir -p $outdir
for k in {2..7};
do
  jellyfish count -m $k -C -s 1000M -o $outdir/k${k}mer_counts.jf $fasta_in
  jellyfish dump $outdir/k${k}mer_counts.jf |tr '\n' '\t'|sed 's/>/\n/g'|grep '\w' > $outdir/k${k}mer_counts.tsv
done
