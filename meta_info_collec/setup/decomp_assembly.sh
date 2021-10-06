datadir=$1
sp=$2

echo -n "zcat fa... "
gzipped=`echo $datadir/$sp/*/assembly/*.fa.gz`
fa=${gzipped%.gz}

zcat $gzipped > $fa

echo -n "zcat gff3... "
gzippedgff=`echo $datadir/$sp/*/annotation/*.gff3.gz`
gff=${gzippedgff%.gz}

zcat $gzippedgff > $gff


