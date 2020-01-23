#! /bin/bash

# generates overlapping single genome plant predictions for a given model
# for the plants, the input length does not vary

if [[ $# -lt 2 ]]; then
	echo "Usage: ./mk-predictions-plants.sh job_folder model_file"
	exit
fi

job_folder=$1
model_file=$2
data_main_folder="/gpfs/project/festi100/data/plants/single_genomes"

# for data_folder in Alyrata  Csativus  Macuminata  Ppatens  Taestivum  Vcarteri; do
for data_folder in $(ls -d "$data_main_folder"/*/); do
	species=$(basename $data_folder)
	job_subfolder=$job_folder/$species
	if [[ ! -d $job_subfolder ]]; then
		mkdir -p $job_subfolder
		qsub_file_path=$job_subfolder/$species".sh"
		cat <<- EOF > $qsub_file_path
		#!/bin/bash
		#PBS -l select=1:ncpus=1:mem=3gb:ngpus=1:accelerator_model=gtx1080ti
		#PBS -l walltime=7:59:00
		#PBS -A "HelixerOpt"

		module load TensorFlow/1.10.0

		##Call, also run again if an error occurs (can happen seemingly at random)
		/home/festi100/git/HelixerPrep/helixerprep/prediction/LSTMModel.py -v -bs 400 -lm $model_file -td $data_main_folder/$species/test_data.h5 -po \$PBS_O_WORKDIR/predictions.h5 --overlap --overlap-offset 2500 --core-length 10000 || /home/festi100/git/HelixerPrep/helixerprep/prediction/LSTMModel.py -v -bs 400 -lm $model_file -td $data_main_folder/$species/test_data.h5 -po \$PBS_O_WORKDIR/predictions.h5 --overlap --overlap-offset 2500 --core-length 10000
		EOF

		echo -n $species" "
		cd $job_subfolder
		qsub $species".sh"

		# sleep 60 # to check everything and spread out the jobs
	else
		echo "Folder $job_subfolder exists. skipping."
	fi
done
