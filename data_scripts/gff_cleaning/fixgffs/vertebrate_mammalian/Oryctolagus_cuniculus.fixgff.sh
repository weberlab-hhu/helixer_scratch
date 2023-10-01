mv ncRNA_filtered.gff3 ncRNA_filtered.gff3.bu2
# random CDS hanging around from BestRefseq
# this part should now be fixed by the filter to has parent
#cat ncRNA_filtered.gff3.bu |grep -v rna-NM_001171292.1 > ncRNA_filtered.gff3
pyton Oryctolagus_cuniculus.secondfix.py > ncRNA_filtered.gff3
