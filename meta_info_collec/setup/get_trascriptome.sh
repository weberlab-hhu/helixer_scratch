#for sp in `ls train`;
datadir=$1
for sp in `ls $datadir`;
do
  echo $sp
  basedir=$datadir/$sp

  fa_in=$basedir/*/assembly/*.fa 
  gz_in=`echo $fa_in.gz`
  fa_in=${gz_in%.gz}
  echo -n "zcat fa... "
  zcat $gz_in > $fa_in
  gff3_in=$basedir/*/annotation/*.gff3
  ggz_in=`echo $gff3_in.gz`
  gff3_in=${ggz_in%.gz}
  echo -n "zcat gff3... "
  zcat $ggz_in > $gff3_in

  anno_dir=${gff3_in%/*.gff3}
  echo "gffread..."
  gffread -g $fa_in -y $anno_dir/protein.fa -w $anno_dir/transcripts.fa \
	  -x $anno_dir/cds.fa $gff3_in

done
#gffread -g ../assembly/Acomosus_321_v3.softmasked.fa -y protein.fa -w transcripts.fa -x cds.fa Acomosus_321_v3.gene_exons.gff3
