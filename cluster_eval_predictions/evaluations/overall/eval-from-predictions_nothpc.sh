#! /bin/bash

# evaluates predictions (what would have been in trial.log files when done with nni)
# from a run that only generated predictions.h5 files in different folders
# this is useful to save time as this step can be done concurrently
# uses eval-from-predictions-one-trial.sh to work concurrently

if [[ $# -lt 2 ]]; then
	echo "Usage: ./eval-from-predictions.sh main_folder output_file_name [--redo]"
	exit
fi

main_folder=$1
output_file_name=$2
source $hppath/venv/bin/activate
ls -d "$main_folder"/*/| xargs -n1 -P8 -I% $hppath/../helixer_scratch/cluster_eval_predictions/evaluations/overall/eval-from-predictions-one-trial.sh % $output_file_name

