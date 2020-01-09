#! /bin/bash
unalias rsync &> /dev/null

echo -e "\n----------------\n"
date
echo

echo -e "\nnni local felix"
rsync -rzt --stats --exclude="predictions.h5" /home/felix/nni nni_local_felix/
rsync -rzt --stats --exclude="predictions.h5" /home/felix/.local/nnictl nni_local_felix/

echo -e "\nnni clc server"
rsync -rzt --stats  --exclude="predictions.h5" felix-stiehler@134.99.200.63:/home/felix-stiehler/nni nni_clc_server/
rsync -rzt --stats  --exclude="predictions.h5" felix-stiehler@134.99.200.63:/home/felix-stiehler/.local/nnictl nni_clc_server/

echo -e "\nnni cluster"
rsync -rzt --stats --exclude="predictions.h5" festi100@hpc.rz.uni-duesseldorf.de:/home/festi100/nni nni_cluster/
rsync -rzt --stats --exclude="predictions.h5" festi100@hpc.rz.uni-duesseldorf.de:/home/festi100/.local/nnictl nni_cluster/

echo -e "\ncluster jobs"
rsync -rzt --stats --exclude="predictions.h5" festi100@hpc.rz.uni-duesseldorf.de:/gpfs/project/festi100/jobs cluster_jobs/
