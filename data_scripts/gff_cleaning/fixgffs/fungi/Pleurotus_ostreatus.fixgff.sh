# hide the original from geenuff --basedir identification
ori=`ls *.gff3.gz`
mv $ori $ori.ori
# orphan (gene-less) tRNA features and their exons removed with
# also, manually added and gene-lacking (plasmid?) coordinate removed with
zcat $ori.ori |grep -v tRNA | grep -v NC_009905.1 > ${ori%.gz}

