# viridiplantae_odb10 
# metazoa_odb9 
# eukaryota_odb10
# busco --list-datasets
# of if all else fails, run once on species with busco --auto-lineage
# but this will check at least bacteria, archae, and EUK, separately; maybe more w/in EUK too

lineage=$1
basedir=$2
sp=$3

for mode in geno tran prot
do 
  bash $metapath/scripts/busco/busco_local.sh $lineage $mode $basedir $sp
done
