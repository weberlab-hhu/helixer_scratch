# note this is more of a record / convenient for me, 
# not a script you should use as-is
# i.e. paths are for my machine
# also assumes the Helixer package and all dependencies are installed 
# (venv already activated, if necessary)
# that and Augustus, and all it's dependencies... you get the idea


fasta_path=$1  # full genome
prediction_path=$2  # Helixer predictions h5
data_path=$3  # Helixer data h5
workingdir=$4  # where all the results land
augustus_sp=$5  # which species should augustus use
extrinsic_config=$6  # extrinsic cfg file for augustus & hints
sp_prefix=$7

helixer_path=/home/ali/repos/github/weberlab-hhu/Helixer
scratch_path=/home/ali/repos/github/weberlab-hhu/helixer_scratch

hintsgff=$workingdir/helixer_hints.gff3

hintsfolder=$workingdir/hints_split
idfolder=$workingdir/id_split
fafolder=$workingdir/fa_split
augfolder=$workingdir/aug_split

for folder in $workingdir $idfolder $fafolder $augfolder
do
  mkdir $folder
done

# make the hints
python $helixer_path/scripts/predictions2hints.py -p $prediction_path \
  -d $data_path -o $hintsgff

# Augustus should generally be ran on chromosomes, not genomes, 
# for several reasons...
# so we will split up both the input genome and hints

# first split the fasta file (every million bps or so, doesn't split sequences)
python $scratch_path/method_comp/running_augustus/conformation_fasta.py \
  -i $fasta_path --nchar 1000000 -o $fafolder/split_

# second pull seqids off above
for item in `ls $fafolder/`;
do 
  cat $fafolder/$item |grep '>'|sed 's/>//g' > $idfolder/${item%.fa}id
done

# third use seqids to split hints 
for item in `ls $idfolder`;
do 
  grep -Fwf $idfolder/$item $hintsgff > $hintsfolder/${item%.id}.gff3; 
done

# finally we can run Augustus (6 at once)
runone() {
  splitfa=$1
  split=${splitfa%.fa}
  augustus --species=$augustus_sp $fafolder/$splitfa --softmasking=1 \
    --extrinsicCfgFile=$extrinsic_config --hintsfile=$hintsfolder/$split.gff3 \
    --gff3=on --UTR=on > $augfolder/$split.gff3
}

ls $fafolder |xargs -n1 -P6 runone 

# concatenate and force the augustus output to be unique
cat $augfolder/*.gff3 > $workingdir/raw.augustus.gff3
python $scratch_path/method_comp/running_augustus/scripts/make_unique_names.py \
  -g $workingdir/raw.augustus.gff3 -p $sp_prefix > $workingdir/augustus.gff3
