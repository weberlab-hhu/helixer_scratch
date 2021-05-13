#! /bin/bash

# test genomes
ls -1 ~/Desktop/raw_data_with_dbs/plants | shuf | xargs -L 1 -I % ~/git/HelixerPrep/export.py --main-db-path ~/Desktop/db_folders/plants --out-dir ~/Desktop/data/plants/single_genomes/% --genomes %

