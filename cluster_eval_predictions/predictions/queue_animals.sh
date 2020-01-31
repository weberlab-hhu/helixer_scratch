#! /bin/bash

while true; do
	for job in ZCPHo ZCPHo_6 duZo1 duZo1_7 lH8Hq lH8Hq_5 home home_5; do
		echo "switching to $job"

		# remove all failed jobs and reset next_line count
		job_folder=/gpfs/project/festi100/jobs/$job
		cd $job_folder
		for species_folder in $(ls -d $job_folder/*/); do
			if [[ ! -f $species_folder/predictions.h5 ]]; then
				rm -rv $species_folder
			fi
		done;
		echo -n "1" > next_line
		echo "$job_folder/next_line reset"

		while true; do
			# queue jobs if theoretically possible
			# 30 jobs seems to be the maximum for now
			if [[ $(qstat -u festi100 | grep CUDA | grep " R " | egrep -c -v "00:00$") -lt 30 ]]; then
				./start_eval.sh /gpfs/project/festi100/models/animals_final/$job".h5" /gpfs/project/festi100/data/animals 120
				if [[ $? -eq 1 ]]; then
					exit 1 # something went very wrong
					# an exit code of 2 signals that the directory already existed, from which we just move on to try the next
				fi
				if [[ $(<next_line) -gt 192 ]]; then
					break
				fi
			else
				echo "found 30 jobs running"
				sleep 120
			fi
		done
	done
done
