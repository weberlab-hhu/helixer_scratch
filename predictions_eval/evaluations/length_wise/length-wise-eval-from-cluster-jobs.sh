#! /bin/bash

# initiates length wise prediction evaluations for all species in a folder
# as would be typical for a job on the cluster
# outputs a picture with the length wise performance and a lot of detailed info
# to stdout, that should hopefully be enough to recover everything without having
# to rerun it

if [[ $# -lt 1 ]]; then
	echo "Usage: ./length-wise-eval-from-cluster-jobs.sh predictions_main_folder"
	exit
fi

predictions_main_folder=$1

for species_folder in $(ls -d "$predictions_main_folder"/*/); do
	species=$(basename $species_folder)
	log_file="$species_folder/*.sh.o*"
	dataset=$(grep "test_data.h5" $log_file| cut -d " " -f3 | tr -d ",'")
	cat <<- EOF > $species_folder/$species"_length_wise_eval.sh"
	#!/bin/bash
	#PBS -l select=1:ncpus=1:mem=2gb
	#PBS -l walltime=3:59:00
	#PBS -A "HelixerOpt"

	module load Python/3.6.5

	/home/festi100/git/HelixerPrep/scripts/errors_position_wise.py -p $species_folder/predictions.h5 -d $dataset -g $species -o $species_folder &> $species_folder/length_wise_eval.log
	EOF

	echo -n $species" "
	cd $species_folder
	qsub $species"_length_wise_eval.sh"

	sleep 1
done

