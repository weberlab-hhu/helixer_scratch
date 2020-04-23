#! /bin/bash

dataset="plants"
folder="./$dataset"
plots_per_page=15
tile="3x"

total_count=$(ls -1 $folder | grep -v "aggregate_comparison.png" | wc -l)
count=1

pwd_folder=$(pwd)
cd $folder

for offset in $(seq 1 $plots_per_page $total_count)
do
	files=$(cat ~/git/helixer_scratch/data_insight/$dataset/genomes_by_n75 | tail +$((offset+1)) | head -$plots_per_page | cut -d "," -f1 | sed -e 's/$/_comparison.png/')
	montage -mode concatenate -tile $tile $files $pwd_folder/"montage_"$dataset$count".png"
	((count++))
done

