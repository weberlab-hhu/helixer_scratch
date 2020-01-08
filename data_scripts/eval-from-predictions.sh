#! /bin/bash

# generates predictions (what would have been in trial.log files when done with nni)
# from a run that only generated predictions.h5 files in different folders
# this is useful to save time as this step can be done concurrently
# uses 16 jobs concurrently by default

if [[ $# -lt 1 ]]; then
	echo "Usage: ./eval-from-predictions.sh main_folder [output file name]"
	exit
fi

main_folder=$1

if [[ $# -lt 2 ]]; then
	output_file_name="trials.log"
else
	output_file_name=$2
fi



