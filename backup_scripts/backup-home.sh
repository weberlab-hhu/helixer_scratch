#! /bin/bash
unalias rsync &> /dev/null

echo
date

rsync -rzt --stats -e 'ssh -A -o "ProxyJump felix@134.99.224.59"' /home/felix/nni-experiments felix@134.99.224.58:/mnt/data/experiments_backup/nni_home_felix/
