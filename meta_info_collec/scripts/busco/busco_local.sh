lineage=$1
mode=$2
basedir=$3
species=$4

#source /home/ali/extra_programs/busco-5.2.2/venv/bin/activate

if [ $mode = "geno" ]; then
    fa_in=$basedir/$species/*/assembly/*.fa 
elif [ $mode = "prot" ]; then
    fa_in=$basedir/$species/*/annotation/protein.fa
elif [ $mode = "tran" ]; then
    fa_in=$basedir/$species/*/annotation/transcripts.fa
else
    echo "unrecognized mode:" $mode
fi

busco_out=$basedir/$species/meta_collection/busco/
tmp_out=tmp_${species}_$mode
#other_tmp_out=tmp/${species}_$mode
#busco_lin=/gpfs/project/alden101/resources/viridiplantae_odb10 # or metazoa_odb9 or eukaryota_odb10
mkdir -p $busco_out

#~/repos/gitlab/ezlab/busco/scripts/run_BUSCO.py -i $fa_in -o $tmp_out -m geno -l $busco_lin -t $other_tmp_out 
busco --in $fa_in --out $tmp_out --mode $mode -l $lineage -f
mv $tmp_out $busco_out/$mode

