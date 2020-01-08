#! /bin/bash

from=/mnt/data/ali/share/phytozome_organized/ready/train
to=~/git/GeenuFF/tmp/$1/input

if [ $# -eq 0 ]; then
	ls $from
else
	if [ ! -d $to ]; then
		mkdir -p $to
		zcat $from/$1/*/assembly/*.fa.gz > $to/$1.fa
		zcat $from/$1/*/annotation/*.gff3.gz > $to/$1.gff3
		echo "unpacked $1"
	else
		echo "Dir exists already"
	fi
fi
