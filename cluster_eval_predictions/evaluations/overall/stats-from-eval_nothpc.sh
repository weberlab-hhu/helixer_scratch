#! /bin/bash

# evaluates predictions (what would have been in trial.log files when done with nni)
# from a run that only generated predictions.h5 files in different folders
# this is useful to save time as this step can be done concurrently
# uses eval-from-predictions-one-trial.sh to work concurrently

if [[ $# -lt 2 ]]; then
	echo "Usage: ./stats-from-eval.sh main_folder output_file_name"
	exit
fi
here=`readlink -f $0`
here=${here%/stats-from-eval*sh}
main_folder=$1
output_file_name=$2

for i in `ls -d "$main_folder"/*/`;
do 
  $here/stats-from-eval-one-trial_nothpc.sh $i  $output_file_name
done

