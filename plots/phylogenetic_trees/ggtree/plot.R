# This code need the ggtree fork from https://github.com/soi/ggtree to run
library(ggplot2)
library(ggtree)
library(treeio)
library(tidytree)

# animals
tree = read.nhx('animals/all_species.tre')

f1_scores = read.csv('animals/f1_scores.csv', header=TRUE)
differences = read.csv('animals/differences.csv', header=TRUE)
sets = read.csv('animals/sets.csv', header=TRUE)

p = ggtree(tree) %<+% sets + geom_tiplab(size=4, offset=.3) + geom_tippoint(aes(color=Set, shape=Set, size=.5)) + guides(size=F) 
# p = p + geom_label(aes(label=node), fill='steelblue')
# p = p + geom_cladelabel(node=201, label="Mammalia", align=T, geom='label', offset=12)

png('animals_differences.png', width=1200, height=3000)
gheatmap(p, differences, width=.1, low="red", mid="white", high="blue", midpoint=0.0, use_scale_fill_gradient2=T, colnames=F, offset=5, legend_title="Difference") 
dev.off()

png('animals_f1_scores.png', width=1200, height=3000)
gheatmap(p, f1_scores, width=.1, colnames=F, offset=5, use_scale_fill_viridis_d=T, legend_title="Subgenic F1")
dev.off()

# plants
tree = read.nhx('plants/all_species.tre')

f1_scores = read.csv('plants/f1_scores.csv', header=TRUE)
differences = read.csv('plants/differences.csv', header=TRUE)
sets = read.csv('plants/sets.csv', header=TRUE)

p = ggtree(tree) %<+% sets + geom_tiplab(size=4, offset=.3) + geom_tippoint(aes(color=Set, shape=Set, size=.5)) + guides(size=F) 
# p = p + geom_label(aes(label=node), fill='steelblue')
# p = p + geom_cladelabel(node=201, label="Mammalia", align=T, geom='label', offset=12)

png('plants_differences.png', width=600, height=900)
gheatmap(p, differences, width=.15, low="red", mid="white", high="blue", midpoint=0.0, use_scale_fill_gradient2=T, colnames=F, offset=5, legend_title="Difference") 
dev.off()

png('plants_f1_scores.png', width=600, height=900)
gheatmap(p, f1_scores, width=.15, colnames=F, offset=5, use_scale_fill_viridis_d=T, legend_title="Subgenic F1") 
dev.off()
