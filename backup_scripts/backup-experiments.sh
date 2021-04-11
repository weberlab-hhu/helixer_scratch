#! /bin/bash
unalias rsync &> /dev/null

echo -e "\n----------------\n"
date
echo

# echo -e "\nnni local felix"
# rsync -rzt --stats --exclude="predictions.h5" /home/felix/nni nni_local_felix/

echo -e "\nnni clc server"
rsync -rzth --stats  --exclude="predictions.h5" felix-stiehler@134.99.200.63:/home/felix-stiehler/nni-experiments nni_clc_server/
