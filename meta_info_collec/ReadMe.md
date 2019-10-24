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
cd $readypath
bash setup/get_transcriptome.sh test
# quast
ls test/|xargs -I% -n1 -P4 bash scripts/quast.sh test %
# count gff features
ls test/|xargs -I% -n1 -P4 bash /home/ali/repos/github/alisandra/helixer_scratch/meta_info_collec/scripts/count_gff.sh test %
```
