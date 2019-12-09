#! /bin/bash
cat ~/Desktop/data_insight/animals/genome_sizes_fragments | tail -n +3 | cut -f1 -d " " | shuf | xargs -P 8 -I % ~/git/HelixerPrep/export.py --db-path-in /mnt/data/felix/animal_geenuff.sqlite3 --out-dir /mnt/data/felix/datasets/animals/single_genomes/% --chunk-size 20000 --skip-meta-info --only-test-set --genomes %
