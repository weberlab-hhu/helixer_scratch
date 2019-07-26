for item in `ls test_import`;
do
	mkdir -p test_import/$item/meta_collection/jellyfish
done

for k in {2..7};
do
  ls test_import |xargs -P 4 -I % ./jellycount.sh % $k 
 
done
