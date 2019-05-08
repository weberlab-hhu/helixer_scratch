for i in `ls`;do j=`echo $i/*/annotation/`;less $j/*gene_exons.gff3.gz|grep -v '^#'|cut -f3|sort |uniq -c > ${j}/counts.txt;done

