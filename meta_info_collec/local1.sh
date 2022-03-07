basedir=$1
sp=$2
lineage=$3

source /home/ali/repos/github/ezlab/busco/venv38/bin/activate
# genome QC
bash $metapath/scripts/quast.sh $basedir $sp
bash $metapath/scripts/count_gff.sh $basedir $sp
# bash $metapath/scripts/kmers.sh $basedir $sp  # I don't think we want to run that still
bash $metapath/scripts/jellyfish.sh $basedir $sp
bash $metapath/scripts/1mers.sh $basedir $sp
if [ $lineage ];then
    bash $metapath/scripts/busco.sh $lineage $basedir $sp
else
    echo "no lineage provided so skipping busco; if this isn't desired maybe add one of viridiplantae_odb10 metazoa_odb9 eukaryota_odb10, or from busco --list-datasets as appropriate"
fi

