#! /bin/bash

trial_id=$1
trial_path="/home/felix-stiehler/nni/experiments/QHKf7JfJ/trials/$1/"

genome=$(cat "$trial_path"parameter.cfg | cut -d "{" -f3 | cut -d "/" -f8)

echo $genome



