datadir=$1
sp=$2  # species
j=`echo $datadir/$sp/*/annotation/`;
outdir=$datadir/$sp/meta_collection/gff_features/
mkdir -p $outdir
less $j/*gene_exons.gff3.gz|grep -v '^#'|cut -f3|sort |uniq -c > $outdir/counts.txt

