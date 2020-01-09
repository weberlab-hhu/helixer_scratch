#! /bin/bash

if [[ $# -lt 1 ]]; then
	echo "Usage: ./start_many.sh n_qsubs"
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

line_offset=$(<next_line)
n_lines=$(cat datasets | wc -l)
if [[ $(($line_offset+$1)) -gt $(($n_lines+1)) ]]; then
	n_qsubs=$(($n_lines-$line_offset+1))
else
	n_qsubs=$1
fi

for i in $(seq 1 $n_qsubs); do
	./start_eval.sh /gpfs/project/festi100/models/ZCPHo_6.h5 /gpfs/project/festi100/data/animals/
done
