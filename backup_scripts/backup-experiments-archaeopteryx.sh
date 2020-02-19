#! /bin/bash
unalias rsync &> /dev/null

echo -e "\n----------------\n"
date
echo

echo -e "\nnni denbi"
rsync -rzt --stats --exclude="predictions.h5" triceratops:nni nni_denbi/
rsync -rzt --stats --exclude="predictions.h5" triceratops:.local/nnictl nni_denbi/

echo -e "\nnni mordred"
rsync -rzt --stats  --exclude="predictions.h5" mordred:nni nni_mordred/
rsync -rzt --stats  --exclude="predictions.h5" mordred:.local/nnictl nni_mordred/
