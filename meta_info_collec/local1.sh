basedir=$1
sp=$2

# genome QC
bash $metapath/scripts/quast.sh $basedir $sp
bash $metapath/scripts/count_gff.sh $basedir $sp
bash $metapath/scripts/kmers.sh $basedir $sp
bash $metapath/scripts/jellyfish.sh $basedir $sp
bash $metapath/scripts/1mers.sh $basedir $sp
