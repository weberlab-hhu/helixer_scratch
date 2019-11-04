datadir=$1
sp=$2

gzipped=`echo $datadir/$sp/*/assembly/*.fa.gz`
fa=${gzipped%.gz}

zcat $gzipped > $fa
