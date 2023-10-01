mv ncRNA_filtered.gff3 ncRNA_filtered.gff3.bu
# not so, does not sound like it's trying to be part of a gene
cat ncRNA_filtered.gff3.bu |grep -v response_element |grep -v enhancer_blocking_element \
  |grep -v imprinting_control_region > ncRNA_filtered.gff3
