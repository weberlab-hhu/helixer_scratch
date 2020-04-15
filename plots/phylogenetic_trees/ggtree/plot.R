library(ggplot2)
library(ggtree)
library(treeio)
library(tidytree)

tree = read.nhx('all_species.tre')
# tree_human = tree_subset(tree, node="Homosapiens", levels_back=5)


f1_scores = read.csv('f1_scores.csv', header=TRUE)
differences = read.csv('differences.csv', header=TRUE)
sets = read.csv('sets.csv', header=TRUE)

p = ggtree(tree) %<+% sets + geom_tiplab(size=4, offset=.3) + geom_tippoint(aes(color=set)) 
# p = p + geom_label(aes(label=node), fill='steelblue')
# p = p + geom_cladelabel(node=201, label="Mammalia", align=T, geom='label', offset=12)

png('animals_differences.png', width=1200, height=2000)
gheatmap(p, differences, width=.2, low="red", mid="white", high="blue", midpoint=0.0, use_scale_fill_gradient2=T, colnames=F, offset=5) 
dev.off()

png('animals_f1_scores.png', width=1200, height=2000)
gheatmap(p, f1_scores, width=.2, low="red", high="blue", colnames=F, offset=5) 
dev.off()
