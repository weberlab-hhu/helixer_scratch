#! /bin/bash

if [[ $# -lt 2 ]]; then
	echo "Usage: ./stats-from-eval-one-trial_nothpc.sh trial_folder eval_file_name"
	exit
fi

trial_folder=$1
eval_file_name=$2

# if the folder has a trial.log in it we assume nni, otherwise cluster
log_file="$trial_folder/$eval_file_name"
dataset=$(cat $log_file| grep -v load_model_path | grep ": '\(.*_data.h5\)'" -o|sed "s/[: ']//g")
model=$(cat $log_file| grep "'load_model_path': '\(.*.h5\)'" -o|sed "s/[: ']//g;s/load_model_path//g")

dataset=${dataset%/*_data.h5}
dataset=`echo $dataset|sed 's@.*/@@g'`

model=`echo $model|sed 's@.*/@@g'`




genicf1=`cat $trial_folder/$eval_file_name |grep '| genic'|sed 's/ //g'|cut -f5 -d'|'`
subgenicf1=`cat $trial_folder/$eval_file_name |grep '| sub_genic'|sed 's/ //g'|cut -f5 -d'|'`

echo "$model,$dataset,$genicf1,$subgenicf1"
