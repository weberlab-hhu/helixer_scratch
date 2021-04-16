#! /bin/bash

for id in tQt2W x9HyB
do
	/home/felix-stiehler/git/HelixerPrep/helixer/prediction/DanQModel.py -v -l /home/felix-stiehler/Desktop/models/"$id".h5 -t /home/felix-stiehler/Desktop/data/plants/nine_genomes_nosplit/training_data.h5 -p /home/felix-stiehler/Desktop/predictions/"$id"_nine_genomes_nosplit_training_data_predictions.h5 --val-test-batch-size 130 --gpu-id 1
done
