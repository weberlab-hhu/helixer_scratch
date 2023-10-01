mv ncRNA_filtered.gff3 ncRNA_filtered.gff3.bu
# remove some random orphan CDS entries that are anyway very similar to an otherwise OK
# gene that is there
cat ncRNA_filtered.gff3.bu|grep -v rna-XM_029491031.1|grep -v rna-NM_001293484.1 |grep -v rna-XM_003246681.4> ncRNA_filtered.gff3
