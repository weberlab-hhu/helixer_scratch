pfx=/mnt/data/helixer_geenuff_share/refseq/fungi/
ls $pfx|grep -v download.log|grep -v index.html| xargs -n1 -P4 bash length_stats1.sh 
