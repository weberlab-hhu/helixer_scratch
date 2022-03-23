here=`pwd`
for dlset in "test" "train";
do
  for item in `cat set_assignments.csv|grep $dlset|sed "s/,$dlset//g"`;
  do
    for sampsize in single_genomes_fungi single_genomes_fungi_downsample800;
    do 
      mkdir -p $dlset/$sampsize/$item;
      cd $dlset/$sampsize/$item;
      ln -s ../../$sampsize/$item/test_data.h5
      cd $here
    done
  done
done
