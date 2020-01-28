#! /bin/bash

# runs ensemble.py for a given number of job folders
# qsubs one job per species
# makes some assumptions about pathnames and folder structures
# outputs the ensembled predictions into a folder that has the concatenated name of the input folders

if [[ $# -lt 2 ]]; then
	echo "Usage: ./ensemble-predictions.sh job_folder1, job_folder2, [job_folder3], .."
	exit
fi

job_main_folder="/gpfs/project/festi100/jobs/"
output_main_folder=$job_main_folder/"ensemble_"$(echo -n $@ | tr " " "_")

for species_folder in $(ls -d "$job_main_folder/$1"/*/); do
	species=$(basename $species_folder)
	output_species_folder=$output_main_folder/$species
	if [[ ! -d $output_species_folder ]]; then
		mkdir -p $output_species_folder

		parameters=" -po "$output_species_folder/"predictions.h5"
		for job_name in $@; do
			parameters=" -p "$job_main_folder/$job_name/$species/"predictions.h5"$parameters
		done

		cat <<- EOF > $output_species_folder/$species"_ensemble.sh"
		#!/bin/bash
		#PBS -l select=1:ncpus=1:mem=200mb
		#PBS -l walltime=3:59:00
		#PBS -A "HelixerOpt"

		module load Python/3.6.5

		/home/festi100/git/HelixerPrep/scripts/ensemble.py$parameters
		EOF

		echo -n $species" "
		cd $output_species_folder
		# qsub $species"_ensemble.sh"

		sleep 2
	else
		echo "Folder "$output_species_folder" already exists."
	fi
done


