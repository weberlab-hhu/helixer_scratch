taxonkit name2taxid <(ls single_genomes_fungi| sed 's/_/ /g') > allspecies.taxid
# as usual, this finds most, but not all species, therefore, ran
# `cp allspecies.taxid allspecies.taxid.fix`
# opened up allspecies.taxid.fix with vim and searched for \W$ (defacto, tab then line break)
# copy pasted the species name for all the species with missing taxids into
# https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi
# and copy pasted the resulting taxid back into allspecies.taxid.fix
# not nice, particularly because they all match anyway, but it's only a 
# handful and choosing ones battles...
wget http://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
mv taxdump.tar.gz ~/.taxonkit/taxdump.tar.gz
source ~/extra_programs/ete-3.1.2/venv/bin/activate

### all species
cut -f2 allspecies.taxid.fix |ete3 ncbiquery --taxdump_file ~/.taxonkit/taxdump.tar.gz --tree > ncbi.tre
# there is extra logging crud, not just the newick in the ncbi.tre file, fix as follows
cat ncbi.tre |grep '(' > ncbi.tree
# and plot
cat ncbi.tree |ete3 view --ncbi --image ncbitree.png
# and record w/ exact names
paste allspecies.taxid.fix <(ls single_genomes_fungi) > name_taxid_ourid.tsv

### now the tree for train only
grep -Fwf <(cat set_assignments.csv|grep ',train'|sed 's/,train//g') name_taxid_ourid.tsv \
  |cut -f2 |ete3 ncbiquery --taxdump_file ~/.taxonkit/taxdump.tar.gz --tree |grep '(' > train.tree
# and plot
cat train.tree |ete3 view --ncbi --image traintree.png


