library(ggplot2)
library(ggtree)
library(treeio)
library(tidytree)

tree = read.nhx('all_species.tre')
# tree_human = tree_subset(tree, node="Homosapiens", levels_back=5)


results = read.csv('f1_scores.csv', header=TRUE)
sets = read.csv('sets.csv', header=TRUE)
p = ggtree(tree) %<+% sets + geom_tiplab(size=4, offset=.3) + geom_tippoint(aes(color=set)) 
# p = p + geom_label(aes(label=node), fill='steelblue')
p = p + geom_cladelabel(node=201, label="Mammalia", align=T, geom='label', offset=12)

png('animals.png', width=1200, height=2000)
gheatmap(p, results, width=.2, low="red", mid="white", high="blue", midpoint=0.8, 
		 colnames=F, offset=5) 
dev.off()
