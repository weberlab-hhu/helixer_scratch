srs=$1

samtools view $srs.bam |python ~/repos/github/alisandra/helixer_scratch/handling_meta/lenN.py  > $srs.introns
cat $srs.introns|uniq > $srs.introns.uniq
Rscript --vanilla ~/repos/github/alisandra/helixer_scratch/handling_meta/intron_histogram.R $srs
