#source /mnt/data/ali/nemicolopterus/ali/Ankylosaurus/Core_projects/Puma/data/Phytozome_dump/Phytozome/venv/bin/activate

datadir=$1
sp=$2

outdir=$datadir/$sp/meta_collection/quoddel/geno
mkdir -p $outdir
zcat $datadir/$sp/*/assembly/*.fa.gz |quoddel > $outdir/report.tsv
