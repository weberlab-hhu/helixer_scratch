#! /bin/bash

trial_id=$1
trial_path="/home/felix-stiehler/nni/experiments/QHKf7JfJ/trials/$1/"
data_path="/home/felix-stiehler/Desktop/data/plants/single_genomes_new/"

genome=$(cat "$trial_path"parameter.cfg | cut -d "{" -f3 | cut -d "/" -f8)

/home/felix-stiehler/git/HelixerPrep/scripts/errors_position_wise.py -p "$trial_path"predictions.h5 -d "$data_path$genome"/test_data.h5 -g $genome &> eval_"$genome"
