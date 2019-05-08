rel_path <- '../PhytozomeV13/'
genomes <- list.files(rel_path)

get_greppable_path  <- function(rel_path, genome, to_grep){
  recursive_paths <- list.dirs(paste0(rel_path, genome))
  out <- recursive_paths[grep(to_grep, recursive_paths)]
  return(out)
}

import_quast <- function(rel_path, genome){
  quast_dir <- get_greppable_path(rel_path, genome, to_grep='quast$')
  quast_path <- paste0(quast_dir, '/report.tsv')
  quast <- read.csv(quast_path, sep='\t')
  return(quast)
}

import_anno_counts <- function(rel_path, genome){
  anno_dir <- get_greppable_path(rel_path, genome, to_grep='annotation$')
  counts_path <- paste0(anno_dir, '/counts.txt')
  counts <- read.table(counts_path, header=FALSE, row.names=2)
  return(counts)
}

meh <- lapply(genomes, function(x) import_quast(rel_path, x))

datatab <- sapply(meh, function(x) x[,2])
rownames(datatab) <- meh[[1]][,1]
colnames(datatab) <- genomes

counts2keep <- c('gene', 'mRNA', 'exon', 'CDS')
annomeh <- lapply(genomes, function(x) import_anno_counts(rel_path, x))
annotab <- sapply(annomeh, function(x) x[counts2keep, 1])
rownames(annotab) <- counts2keep
colnames(annotab) <- genomes

datatab <- rbind(datatab, annotab)

