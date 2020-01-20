#! /bin/bash

# evaluates predictions (what would have been in trial.log files when done with nni)
# from a run that only generated predictions.h5 files in different folders
# this is useful to save time as this step can be done concurrently
# uses eval-from-predictions-one-trial.sh to work concurrently
# concurrency default is set to 16 currently

if [[ $# -lt 2 ]]; then
	echo "Usage: ./eval-from-predictions.sh main_folder output_file_name [--redo]"
	exit
fi

main_folder=$1
output_file_name=$2

for species_folder in $(ls -d "$main_folder"/*/); do
	species=$(basename $species_folder)
	output_file_path=$species_folder/$output_file_name
	if [[ $# -lt 3 || ($3 == '--redo' && (! -f $output_file_path || ! -s $output_file_path)) ]]; then
		cat <<- EOF > $species_folder/$species"_eval.sh"
		#!/bin/bash
		#PBS -l select=1:ncpus=1:mem=500mb
		#PBS -l walltime=3:59:00
		#PBS -A "HelixerOpt"

		module load Python/3.6.5

		/home/festi100/git/helixer_scratch/data_scripts/eval-from-predictions-one-trial.sh $species_folder $output_file_name
		EOF

		echo -n $species" "
		cd $species_folder
		qsub $species"_eval.sh"
	else
		echo $species" skipped"
	fi

	sleep 1 # to check everything
done
