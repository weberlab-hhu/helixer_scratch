#! /bin/bash
unalias rsync &> /dev/null

echo -e "\n----------------\n"
date
echo

echo -e "\nnni denbi no longer active"
#rsync -rzt --stats --exclude="predictions.h5" triceratops:nni nni_denbi/
#rsync -rzt --stats --exclude="predictions.h5" triceratops:.local/nnictl nni_denbi/

echo -e "\nnni mordred"
rsync -rzt --stats  --exclude="predictions.h5" mordred:nni nni_mordred/
rsync -rzt --stats  --exclude="predictions.h5" mordred:.local/nnictl nni_mordred/

echo -e "\nnni aardonyx"
rsync -rzt --stats  --exclude="predictions.h5" aardonyx:nni nni_aliclc/
rsync -rzt --stats  --exclude="predictions.h5" aardonyx:.local/nnictl nni_aliclc/

echo -e "\nhpc"
rsync -rzt --stats  --exclude="predictions.h5" hpc:/gpfs/scratch/alden101/training ali_hpc/

echo -e "\nnni local"
rsync -rzt --stats  --exclude="predictions.h5" $HOME:nni troodon:/mnt/data/experiments_backup/nni_archaeopteryx/
rsync -rzt --stats  --exclude="predictions.h5" $HOME:.local/nnictl troodon:/mnt/data/experiments_backup/nni_archaeopteryx/



