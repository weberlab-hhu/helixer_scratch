library(ggplot2)
library(ggtree)
library(treeio)
library(tidytree)

tree = read.nhx('all_species.tre')
# tree_human = tree_subset(tree, node="Homosapiens", levels_back=5)


f1_difference = read.csv('f1_difference.csv', header=TRUE)
p = ggtree(tree) + geom_tiplab(size=4)

png('animals.png', width=800, height=2000)
gheatmap(p, f1_difference, width=.3, high='darkgreen', low='red', colnames=F, offset=9)
dev.off()




