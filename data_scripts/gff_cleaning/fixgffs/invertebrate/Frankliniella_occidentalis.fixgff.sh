mv ncRNA_filtered.gff3 ncRNA_filtered.gff3.bu
# repace the orphan cDNA_match features with a gene
# as a hackish solution to force an empty superlocus 
# feature and get them masked by geenuff
cat ncRNA_filtered.gff3.bu |sed 's/cDNA_match/gene/g' > ncRNA_filtered.gff3
