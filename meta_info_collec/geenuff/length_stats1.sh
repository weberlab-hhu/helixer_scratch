sp=$1
outpath=/mnt/data/helixer_geenuff_share/refseq/fungi/$sp/meta_collection/geenuff/
mkdir $outpath
for mode in mRNA pre-mRNA CDS exons introns UTR pre-UTR intergenic;
do
  python /home/ali/repos/github/weberlab-hhu/GeenuFF/scripts/dump_lengthinfo.py \
  --db-path-in $sp/output/$sp.sqlite3 -m $mode --longest --stats-only > $outpath/longest_$mode.tsv
  python /home/ali/repos/github/weberlab-hhu/GeenuFF/scripts/dump_lengthinfo.py \
  --db-path-in $sp/output/$sp.sqlite3 -m $mode --stats-only > $outpath/all_$mode.tsv
done
