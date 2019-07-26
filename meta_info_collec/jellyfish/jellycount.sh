#!/bin/bash
sp=$1
k=$2
fasta_in=`echo test_import/$sp/input/*.fa`
jellyfish count -m $k -C -s 1000M -o test_import/$sp/meta_collection/jellyfish/k${k}mer_counts.jf $fasta_in
