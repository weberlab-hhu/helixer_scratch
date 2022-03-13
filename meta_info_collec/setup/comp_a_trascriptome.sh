datadir=$1
sp=$2
echo $sp
basedir=$datadir/$sp
# assumes existing fa
fa_in=`echo $basedir/*/assembly/*.fa`
# assumes extracted gff
gff3_in=`echo $basedir/*/annotation/*.gff3`


anno_dir=${gff3_in%/*.gff3}
echo "compressing in $anno_dir"
gzip $anno_dir/cds.fa
gzip $anno_dir/transcripts.fa
gzip $anno_dir/protein.fa

