datadir=$1
sp=$2

# decompress fa
gzipped=`echo $datadir/$sp/*/assembly/*.fa.gz`
fa=${gzipped%.gz}
kmerdir=$datadir/$sp/meta_collection/kmers/
#zcat $gzipped > $fa

# count kmers
mkdir -p $kmerdir
python $metapath/kmers/count_kmers.py \
	--min_k 1 --max_k 3 $fa > $kmerdir/kmers.tsv

# gzip kmers
gzip $kmerdir/kmers.tsv

# could clean up fa, but busco needs it too
#rm $fa
