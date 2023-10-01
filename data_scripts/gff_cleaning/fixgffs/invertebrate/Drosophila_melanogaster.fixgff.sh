mv ncRNA_filtered.gff3 ncRNA_filtered.gff3.bu
# there is one weird 'partial gene' that has several (overlapping?) loci on different
# strands. The following will grep away all the crash causing features with a '?'
# in the strand field, and all other child features; which will allow it to parse,
# but leave a mask for an empti super loci that remain ([^g])
cat ncRNA_filtered.gff3.bu|grep -v 'ID=[^g].*Dmel_CG32491' > ncRNA_filtered.gff3
