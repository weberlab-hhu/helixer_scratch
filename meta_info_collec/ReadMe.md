# meta-info
as much as possible I will be trying to setup scripts so that they can be run with 

```
ls data_dir|xargs script.sh
```

Or with a job array for qsub in a similar fashion I guess.

Obviously they will need some parameters here and there, that will get names.

I will probably be copying the scripts here (for the sake of having an organized
record) after using them, but one might find originals stored with the data.


## test (first attempt to run a second time

```
metapath=/home/ali/repos/github/alisandra/helixer_scratch/meta_info_collec/
cd $readypath
bash setup/get_transcriptome.sh test
# fix stop codons in proteome
for i in `ls test`; 
do 
  python scripts/fix_stopcodons.py -i test/$i/*/annotation/protein.fa -o tmpprotein$i.fa;
  mv tmpprotein$i.fa test/$i/*/annotation/protein.fa;
done

# quast
# todo, insert activate quast venv?
ls test/|xargs -I% -n1 -P4 bash scripts/quast.sh test %
# count gff features
ls test/|xargs -I% -n1 -P4 bash $metapath/scripts/count_gff.sh test %

# kmers
deactivate
source ~/repos/venv/bin/activate
ls test/|xargs -n1 -P4 bash $metapath/scripts/kmers.sh test 

```

## improved org

```
# e.g. 
basedir=test
ls $basedir/ | xargs -n1 -P6 bash $metapath/prep1.sh $basedir
ls $basedir/ | xargs -n1 -P6 bash $metapath/local1.sh $basedir
```
