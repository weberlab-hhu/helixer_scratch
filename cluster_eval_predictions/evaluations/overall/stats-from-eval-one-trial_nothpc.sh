#! /bin/bash

if [[ $# -lt 2 ]]; then
	echo "Usage: ./stats-from-eval-one-trial_nothpc.sh trial_folder eval_file_name"
	exit
fi

trial_folder=$1
eval_file_name=$2

# if the folder has a trial.log in it we assume nni, otherwise cluster
if [[ -f "$trial_folder/trial.log" ]]; then
	log_file="$trial_folder/trial.log"
	dataset=$(grep "test_data.h5" $log_file| cut -d " " -f5 | tr -d "'")
else
	log_file="$trial_folder/*.sh.o*"
	dataset=$(grep "test_data.h5" $log_file| cut -d " " -f3 | tr -d ",'")
fi

dataset=${dataset%/test_data.h5}
dataset=`echo $dataset|sed 's@.*/@@g'`

genicf1=`cat $trial_folder/$eval_file_name |grep '| genic'|sed 's/ //g'|cut -f5 -d'|'`
subgenicf1=`cat $trial_folder/$eval_file_name |grep '| sub_genic'|sed 's/ //g'|cut -f5 -d'|'`

echo "$dataset,$genicf1,$subgenicf1"
