#! /bin/bash

if [[ $# -lt 1 ]]; then
	echo "Usage: ./augustus_eval.sh main_folder"
	exit
fi

main_folder=$1

for species_folder in $(ls -d "$main_folder"/*/); do
	if [[ -f $species_folder/confusion_matrix.csv ]]; then
		~/git/helixer_scratch/data_scripts/augustus_eval_convert.py $species_folder > $species_folder/eval.log
		echo $(basename $species_folder)
	else
		echo $(basename $species_folder)" was empty"
	fi
done
