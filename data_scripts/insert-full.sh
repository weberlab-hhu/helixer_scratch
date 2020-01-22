#! /bin/bash

# db_path='/mnt/data/felix/animal_geenuff.sqlite3'
db_path='/home/felix/Desktop/animal_geenuff_test.sqlite3'

ls -1 /mnt/data/ali/share/ensembl_test | xargs -I % /home/felix/git/helixer_scratch/data_scripts/insert-one.sh % $db_path

# ge; ls -1 /mnt/data/ali/share/phytozome_organized/ready/test | xargs -I % ./import_genome.py --db-path ~/Desktop/geenuff_plants.sqlite3 --basedir /mnt/data/felix/rawdata/plants/%/ --species %
