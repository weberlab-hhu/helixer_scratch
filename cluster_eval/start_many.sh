#! /bin/bash

if [[ $# -lt 3 ]]; then
	echo "Usage: ./start_many.sh model_file main_data_folder n_qsubs"
	exit
fi

if [[ ! -f "next_line" ]]; then
	echo "next_line file not found. Script has to be run from the root dir."
	exit
fi

if [[ $(basename $(pwd)) = "cluster_eval" ]]; then
	echo "script seems to be run from the repository, which should be an error"
	exit
fi

model_file=$1
main_data_folder=$2

line_offset=$(<next_line)
n_lines=$(cat datasets | wc -l)
if [[ $(($line_offset+$1)) -gt $(($n_lines+1)) ]]; then
	n_qsubs=$(($n_lines-$line_offset+1))
else
	n_qsubs=$3
fi

for i in $(seq 1 $n_qsubs); do
	./start_eval.sh $model_file $main_data_folder
done