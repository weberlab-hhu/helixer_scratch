cat train/*/meta.ini test/*/meta.ini|grep 'species'|sed 's/species=//g' > allspecies.txt
taxonkit name2taxid allspecies.txt > allspecies.taxid
# had to manually fix Micromonas sp. RCC299 - 296587
cut -f2 allspecies.taxid |ete3 ncbiquery --taxdump_file ~/.taxonkit/taxdump.tar.gz --tree > ncbi.tre
# test tre
cat ncbi.tre |ete3 view --ncbi --image ncbitree.png
# had to do some manual mod on some species names still...
