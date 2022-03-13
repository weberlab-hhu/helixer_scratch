datadir=$1
sp=$2

echo -n "cleaning decompressed fa and gff3 from $datadir/$sp"
gzipped=`echo $datadir/$sp/*/assembly/*.fa.gz`
fa=${gzipped%.gz}

rm $fa

gzippedgff=`echo $datadir/$sp/*/annotation/*.gff3.gz`
gff=${gzippedgff%.gz}

rm $gff


