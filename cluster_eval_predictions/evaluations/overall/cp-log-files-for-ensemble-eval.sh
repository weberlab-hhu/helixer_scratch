#! /bin/bash

# An evaluation dependes on a {species}.sh.o* file to be present so it knows where for which
# data file the predictions were made. In case of an ensemble those files are not there
# and need to be copied from one of the ensemble job folders.

if [[ $# -lt 2 ]]; then
	echo "Usage: ./cp-log-files-for-ensemble-eval ensemble_folder job_folder"
	exit
fi

ensemble_folder=$1
job_folder=$2

cd $job_folder
ls -1 -d */ | tr -d "/" | xargs -I % bash -c "cp -v $job_folder/%/%.sh.o* $ensemble_folder/%/"
