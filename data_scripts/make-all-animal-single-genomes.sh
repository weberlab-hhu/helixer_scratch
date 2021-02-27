#! /bin/bash

# len_in_k=$1
# n_processes=$2

# cat ~/Desktop/data_insight/animals/genome_sizes_fragments | tail -n +3 | cut -f1 -d " " | shuf | xargs -P 8 -I % ~/git/HelixerPrep/export.py --db-path-in /mnt/data/felix/animal_geenuff.sqlite3 --out-dir /mnt/data/felix/datasets/animals/single_genomes/% --chunk-size 20000 --only-test-set --genomes %

# test data
# ls -1 /mnt/data/ali/share/ensembl_test | xargs -P $n_processes -I % ~/git/HelixerPrep/export.py --db-path-in ~/Desktop/animal_geenuff_test.sqlite3 --out-dir ~/Desktop/data/animals/single_genomes_"$len_in_k"k/% --chunk-size "$len_in_k"000 --only-test-set --genomes %

test_genomes="apteryx_rowi     choloepus_hoffmanni  danio_rerio   junco_hyemalis  maylandia_zebra        nannospalax_galili      numida_meleagris    pundamilia_nyererei  scophthalmus_maximus  zonotrichia_albicollis calidris_pugnax  cyanistes_caeruleus  gadus_morhua  macaca_mulatta  monodelphis_domestica  nothoprocta_perdicaria  oryzias_melastigma  rattus_norvegicus    serinus_canaria"
for len_in_k in 20 50 100 200; do
	echo $test_genomes | tr " " '\n' | xargs -P 4 -I % ~/git/HelixerPrep/export.py --db-path-in ~/Desktop/animal_geenuff_test.sqlite3 --out-dir ~/Desktop/data/animals/single_genomes_"$len_in_k"k/% --chunk-size "$len_in_k"000 --only-test-set --genomes %
done
