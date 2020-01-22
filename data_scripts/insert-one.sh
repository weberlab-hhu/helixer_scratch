#! /bin/bash

geenuff_basedir=~/git/GeenuFF
data_basedir=/mnt/data/ali/share/ensembl_test
# data_basedir=/mnt/data/ali/share/ensembl_nosplit
# data_basedir=/mnt/data/ali/share/phytozome_organized/ready/test
genome=$1
db_path=$2

rm -v -r $geenuff_basedir/tmp
mkdir -v -p $geenuff_basedir/tmp/input $geenuff_basedir/tmp/output

# gunzip -v -c $data_basedir/$genome/ensembl98/annotation/*.gff3.gz > $geenuff_basedir/tmp/input/$genome.gff3
# gunzip -v -c $data_basedir/$genome/ensembl98/assembly/*.fa.gz > $geenuff_basedir/tmp/input/$genome.fa

cp -v $data_basedir/$genome/ensembl98/annotation/*.gff3 $data_basedir/$genome/ensembl98/assembly/*.fa $geenuff_basedir/tmp/input/

$geenuff_basedir/import_genome.py --db-path $2 --basedir $geenuff_basedir/tmp/ --species $genome
