for sp in `ls test_import`
do
  
  for k in {2..7};
  do
    basedir=test_import/$sp/meta_collection/jellyfish/
    jellyfish dump $basedir/k${k}mer_counts.jf |tr '\n' '\t'|sed 's/>/\n/g'|grep '\w' > $basedir/k${k}mer_counts.tsv 
  done
done
