# setup all raw or derived input files for one species
basedir=$1
sp=$2

bash $metapath/setup/get_a_trascriptome.sh $basedir $sp
bash $metapath/setup/decomp_assembly.sh $basedir $sp
