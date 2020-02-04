#! /bin/bash

# make local predictions on a set of animals

animals_datasets_base="/mnt/data/datasets/animals/"
job_id="duZo1"
model="/home/felix/Desktop/models/animals_final/"$job_id".h5"
predictions_folder_base="/mnt/data/predictions/"$job_id

# for line in $(<~/git/helixer_scratch/cluster_eval_predictions/predictions/animals/cluster/datasets); do
for line in $(egrep "microcebus_murinus|dromaius_novaehollandiae|esox_lucius|mola_mola|lepisosteus_oculatus|erpetoichthys_calabaricus|saimiri_boliviensis_boliviensis" ~/git/helixer_scratch/cluster_eval_predictions/predictions/animals/cluster/datasets); do
	species=$(echo -n $line | cut -d, -f1)
	length=$(echo -n $line | cut -d, -f2)

	data_dir=$animals_datasets_base"/single_genomes_"$length"k/"$species
	predictions_dir=$predictions_folder_base/$species
	mkdir -v -p $predictions_dir

	case $length in
		20)
			batch_size=200
			overlap_offset=2500
			core_length=10000
			;;
		50)
			batch_size=80
			overlap_offset=6250
			core_length=25000
			;;
		100)
			batch_size=40
			overlap_offset=12500
			core_length=50000
			;;
		200)
			batch_size=24
			overlap_offset=25000
			core_length=100000
			;;
		*)
			echo "unknown length"
			exit 1
			;;
	esac

	# make predictions
	/home/felix/git/HelixerPrep/helixerprep/prediction/LSTMModel.py -v -bs $batch_size -lm $model -td $data_dir/test_data.h5 -po $predictions_dir/predictions.h5 --overlap --overlap-offset $overlap_offset --core-length $core_length

	# upload to the cluster in the background
	rsync -r -v $predictions_dir festi100@hpc.rz.uni-duesseldorf.de:/gpfs/project/festi100/jobs/$job_id/ &
done
