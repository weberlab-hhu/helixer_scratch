#! /bin/bash

# download only the test_data.h5 files of the length per animal that is actually needed
# for prediction according to the datasets file

animals_datasets_base="/mnt/data/datasets/animals/"

# for line in $(<~/git/helixer_scratch/cluster_eval_predictions/predictions/animals/cluster/datasets); do
for line in $(egrep "microcebus_murinus|dromaius_novaehollandiae|esox_lucius|mola_mola|lepisosteus_oculatus|erpetoichthys_calabaricus|saimiri_boliviensis_boliviensis" ~/git/helixer_scratch/cluster_eval_predictions/predictions/animals/cluster/datasets); do
	species=$(echo -n $line | cut -d, -f1)
	length=$(echo -n $line | cut -d, -f2)

	species_dir=$animals_datasets_base"/single_genomes_"$length"k/"$species
	mkdir -v -p $species_dir

	# download from the clc
	rsync --progress felix-stiehler@134.99.200.63:/home/felix-stiehler/Desktop/data/animals/single_genomes_$length"k/"$species/test_data.h5 $species_dir/
done
