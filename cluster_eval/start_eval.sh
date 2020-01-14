#! /bin/bash

# reads and removes a line from the datasets file
# fills the qsub template according to the content of that line
# and qsubs a job

if [[ $# -lt 2 ]]; then
	echo "Usage: ./start_eval model_path datasets_basepath"
	exit
fi

if [[ ! -f "next_line" ]]; then
	echo "next_line file not found. Script has to be run from the root dir."
	exit
fi

line_offset=$(<next_line)
if [[ $line_offset -gt $(cat datasets | wc -l) ]]; then
	echo "Line offset $line_offset is too large. Maybe everything is done already."
	exit
fi

model=$1
datasets_basepath=$2
line_content=$(sed -n "$line_offset"p datasets)
species=$(echo -n $line_content | cut -d "," -f1)
eval_len=$(echo -n $line_content | cut -d "," -f2)

if [[ -d $species ]]; then
	echo "$species directory already existing. exiting."
	exit
fi

mkdir $species
cp qsub_template $species/$species".sh"
cd $species

# set length specific params
# we could put this into a config file but for now this should work
declare -A values
if [[ "$eval_len" == "20" ]]; then
	values[__BATCH_SIZE__]="30"
	values[__OVERLAP_OFFSET__]="2500"
	values[__CORE_LENGTH__]="10000"
elif [[ "$eval_len" == "50" ]]; then
	values[__BATCH_SIZE__]="12"
	values[__OVERLAP_OFFSET__]="6250"
	values[__CORE_LENGTH__]="25000"
elif [[ "$eval_len" == "100" ]]; then
	values[__BATCH_SIZE__]="6"
	values[__OVERLAP_OFFSET__]="12500"
	values[__CORE_LENGTH__]="10000"
elif [[ "$eval_len" == "200" ]]; then
	values[__BATCH_SIZE__]="3"
	values[__OVERLAP_OFFSET__]="25000"
	values[__CORE_LENGTH__]="100000"
else
	echo "Unknown length $eval_len. exiting."
	exit
fi

# general params
values[__CPUS__]="1"
values[__MEM__]="3"
values[__GPUS__]="1"
values[__MODEL__]="$model"
values[__TEST_DATA__]="$datasets_basepath""/single_genomes_""$eval_len""k/$species/test_data.h5"

# escape paths so they can be used with sed
for key in __MODEL__ __TEST_DATA__; do
	values[$key]=$(echo -n ${values[$key]} | sed -e 's/\//\\\//g')
done

# insert and print config
for key in "${!values[@]}"; do
	echo "$key:${values[$key]}"
	sed -i -e "s/$key/${values[$key]}/g" $species".sh"
done
echo "line offset: $line_offset"

# qsub
qsub $species".sh"
echo "job queued"

# increment line number
echo -n $((line_offset+1)) > ../next_line
echo "line number incremented"
