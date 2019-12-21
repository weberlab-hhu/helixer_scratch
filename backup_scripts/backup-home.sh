#! /bin/bash
unalias rsync &> /dev/null

echo
date

if [ $(ifconfig -a | grep -c tun0) == 1 ]
then
	rsync -rzt --stats -e 'ssh -A -o "ProxyJump felix@134.99.224.62"' /home/felix/nni felix@134.99.224.58:/mnt/data/experiments_backup/nni_home_felix/
	rsync -rzt --stats -e 'ssh -A -o "ProxyJump felix@134.99.224.62"' /home/felix/.local/nnictl felix@134.99.224.58:/mnt/data/experiments_backup/nni_home_felix/
else
	echo "Not connected to the vpn, writing data to the cluster"
	rsync -rzt --stats --exclude='*model*.h5' /home/felix/nni festi100@hpc.rz.uni-duesseldorf.de:/gpfs/project/festi100/backup_home/
	rsync -rzt --stats /home/felix/.local/nnictl festi100@hpc.rz.uni-duesseldorf.de:/gpfs/project/festi100/backup_home/
fi
