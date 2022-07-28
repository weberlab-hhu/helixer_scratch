# note this is more of a record / convenient for me, 
# not a script you should use as-is
# i.e. paths are for my machine
# that and Augustus, and all it's dependencies are installed... you get the idea


fasta_path=$1  # full genome
workingdir=$2  # where all the results land
export augustus_sp=$3  # which species should augustus use
sp_prefix=$4

helixer_path=/home/ali/repos/github/weberlab-hhu/Helixer
scratch_path=/home/ali/repos/github/weberlab-hhu/helixer_scratch

export fafolder=$workingdir/fa_split
export augfolder=$workingdir/aug_split

for folder in $workingdir $fafolder $augfolder
do
  mkdir $folder
done


# Augustus should generally be ran on chromosomes, not genomes, 
# for several reasons...
# so we will split up both the input genome and hints

# first split the fasta file (every million bps or so, doesn't split sequences)
python $scratch_path/method_comp/running_augustus/scripts/conformation_fasta.py \
  -i $fasta_path --nchar 1000000 -o $fafolder/split_

# we would like to use the UTR models wherever they are available...
if [[ -f $AUGUSTUS_CONFIG_PATH/species/$augustus_sp/${augustus_sp}_utr_probs.pbl ]]; 
then 
  echo "${augustus_sp}_utr_probs.pbl found, UTR on" > $workingdir/utr.info
  export utr=on
else
  echo "${augustus_sp}_utr_probs.pbl missing, UTR off" > $workingdir/utr.info
  export utr=off
fi

# finally we can run Augustus (6 at once)
runone() {
  splitfa=$1
  split=${splitfa%.fa}
  augustus --species=$augustus_sp $fafolder/$splitfa --softmasking=1 \
    --noInFrameStop=true --stopCodonExcludedFromCDS=false \
    --gff3=on --UTR=$utr > $augfolder/$split.gff3
}

export -f runone

ls $fafolder |xargs -I% -n1 -P6 bash -c 'runone %'

# concatenate and force the augustus output to be unique
cat $augfolder/*.gff3 > $workingdir/raw.augustus.gff3
python $scratch_path/method_comp/running_augustus/scripts/make_unique_names.py \
  -g $workingdir/raw.augustus.gff3 -p $sp_prefix > $workingdir/augustus.gff3
