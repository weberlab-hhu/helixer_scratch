assign_sets <- function(unrestricteds, test_fraction=0.1){
  n_unrestricted <- table(unrestricteds)[2]
  n_test <- round(n_unrestricted * test_fraction) 
  n_train <- n_unrestricted - n_test
  scrambled <- c(rep("test", n_test),
		 rep("train", n_train))
  scrambled <- sample(scrambled)

  i <- 1
  out <- c()
  for (item in unrestricteds){
    if (! item){
      out <- c(out, 'someday_test')
    }else{
      out <- c(out, scrambled[i])
      i <- i + 1
    }
  }
  return(out)
}

# import table of data restrictions
restrictions <- read.csv('genome_source_data_phytozome_restrictions.csv')

toplot <- datatab
toplot <- log(toplot + 1)
toplot <- t(scale(t(toplot)))

pc <- prcomp(t(toplot))
pci <- data.frame(pc$x, species=rownames(pc$x))
pci <- merge(pci, restrictions, by.x="species", by.y="genome.name")

set.seed(29185)
for (i in seq(0, 9, 1)){
  pci[[paste0("split", i)]] <- assign_sets(pci$unrestricted)

}

write.csv(pci, file='accept_split9.csv')
