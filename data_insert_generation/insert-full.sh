#! /bin/bash

db_path='/mnt/data/felix/animal_geenuff.sqlite3'

rm -v $db_path;
ls -1 /mnt/data/ali/share/ensembl_nosplit/ | xargs -I % ~/Desktop/data_scripts/insert-one.sh % $db_path

# ge; ls -1 /mnt/data/ali/share/phytozome_organized/ready/train | xargs -I % ./import_genome.py --db-path ~/Desktop/geenuff_plants.sqlite3 --basedir /mnt/data/felix/rawdata/plants/%/ --species %
