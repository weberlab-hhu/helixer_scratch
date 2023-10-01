mv ncRNA_filtered.gff3 ncRNA_filtered.gff3.bu
# meiotic_recombination_region is not in SO, but clearly also has nothing to do with
# protein coding genes
cat ncRNA_filtered.gff3.bu|grep -v meiotic_recombination_region |grep -v repeat_instability_region \
 |sed 's/DNaseI_hypersensitive_site/DNAseI_hypersensitive_site/g'|grep -v non_allelic_homologous_recombination_region \
 | grep -v enhancer_blocking_element |grep -v response_element |grep -v sequence_comparison |grep -v mitotic_recombination_region \
 | grep -v imprinting_control_region |grep -v replication_start_site|grep -v nucleotide_cleavage_site > ncRNA_filtered.gff3

# used debug.py after getting tired finding them one at a time (~sequence_comparison)  to get the rest
#unknown type mitotic_recombination_region
#unknown type imprinting_control_region
#unknown type replication_start_site
#unknown type nucleotide_cleavage_site

