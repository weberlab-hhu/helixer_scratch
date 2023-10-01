# hide the original from geenuff --basedir identification
mv GCF_000226545.1_ASM22654v1_genomic.gff3.gz GCF_000226545.1_ASM22654v1_genomic.gff3.gz.ori
# orphan (gene-less) tRNA features and their exons removed with
zcat GCF_000226545.1_ASM22654v1_genomic.gff3.gz.ori |grep -v tRNA > GCF_000226545.1_ASM22654v1_genomic.gff3
