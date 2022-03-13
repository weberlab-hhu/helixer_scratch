# setup all raw or derived input files for one species
basedir=$1
sp=$2

bash $metapath/setup/comp_a_trascriptome.sh $basedir $sp
bash $metapath/setup/rm_decomp_assembly.sh $basedir $sp
# todo, cleanup extra files from busco, and similar
