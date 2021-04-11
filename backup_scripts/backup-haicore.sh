#! /bin/bash
unalias rsync &> /dev/null

echo
date

if [[ "$#" -ne 1 ]]; then
	echo "need nni id"
	exit
fi

rsync -rztv --stats --exclude "predictions.h5" --exclude "model*.h5" -e 'ssh -A -o "ProxyJump hhu_gateway"' /home/felix/nni-experiments/$1 work_pc:/mnt/data/experiments_backup/nni_haicore/
