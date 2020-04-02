library(ggplot2)
library(ggtree)
library(treeio)
library(tidytree)

tree = read.nhx('~/git/helixer_scratch/plots/phylogenetic_trees/all_species.tre')
tree_human = tree_subset(tree, node="Homosapiens", levels_back=5)


additional_data = read.csv('~/git/helixer_scratch/plots/phylogenetic_trees/additional_data.csv', header=TRUE)
ggtree(tree_human) %<+% additional_data + geom_tiplab(size=2)
gheatmap(p, additional_data, high='darkgreen', low='red', colnames=F)




