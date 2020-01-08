#! /bin/bash
cat ~/git/helixer_scratch/data_insight/plants/genome_names | shuf | xargs -I % -P 2 ~/git/HelixerPrep/export.py --db-path-in ~/Desktop/plant_geenuff.sqlite3 --out-dir ~/Desktop/data/plants/single_genomes_new/% --genomes % --chunk-size 20000 --only-test-set
