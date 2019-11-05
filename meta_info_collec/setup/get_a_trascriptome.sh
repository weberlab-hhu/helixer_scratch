datadir=$1
sp=$2
echo $sp
basedir=$datadir/$sp
# assumes existing fa
fa_in=`echo $basedir/*/assembly/*.fa`
# assumes extracted gff
gff3_in=`echo $basedir/*/annotation/*.gff3`


anno_dir=${gff3_in%/*.gff3}
echo "gffread..."
gffread -g $fa_in -y $anno_dir/broken_protein.fa -w $anno_dir/transcripts.fa \
  -x $anno_dir/cds.fa $gff3_in

# . -> * 4 stop codons
python $metapath/scripts/fix_stopcodons.py -i $anno_dir/broken_protein.fa -o $anno_dir/protein.fa &&
rm $anno_dir/broken_protein.fa
