#! /bin/bash

if [[ $# -lt 2 ]]; then
	echo "Usage: ./eval-from-predictions-one-trial.sh trial_folder output file name"
	exit
fi

trial_folder=$1
output_file_name=$2

# if the folder has a trial.log in it we assume nni, otherwise cluster
if [[ -f "$trial_folder/trial.log" ]]; then
	log_file="$trial_folder/trial.log"
	dataset=$(grep "test_data.h5" $log_file| cut -d " " -f5 | tr -d "'")
else
	log_file="$trial_folder/*.sh.o*"
	dataset=$(grep "test_data.h5" $log_file| cut -d " " -f3 | tr -d ",'")
fi

$hppath/HelixerPrep/scripts/basic_pred_cm.py -d $dataset -p "$trial_folder/predictions.h5" &>> "$trial_folder/$output_file_name"
