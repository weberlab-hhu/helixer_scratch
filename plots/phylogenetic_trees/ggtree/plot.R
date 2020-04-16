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

p = ggtree(tree) %<+% sets + geom_tiplab(size=4, offset=.3) + geom_tippoint(aes(color=set, shape=set, size=.5)) 
# p = p + geom_label(aes(label=node), fill='steelblue')
# p = p + geom_cladelabel(node=201, label="Mammalia", align=T, geom='label', offset=12)

png('animals_differences.png', width=1200, height=2000)
gheatmap(p, differences, width=.1, low="red", mid="white", high="blue", midpoint=0.0, use_scale_fill_gradient2=T, colnames=F, offset=5) 
dev.off()

png('animals_f1_scores.png', width=1200, height=2000)
gheatmap(p, f1_scores, width=.1, low="red", high="darkgreen", colnames=F, offset=5) 
dev.off()



# plants
tree = read.nhx('plants/all_species.tre')

# f1_scores = read.csv('plants/f1_scores.csv', header=TRUE)
# differences = read.csv('plants/differences.csv', header=TRUE)
# sets = read.csv('plants/sets.csv', header=TRUE)

# p = ggtree(tree) %<+% sets + geom_tiplab(size=4, offset=.3) + geom_tippoint(aes(color=set, shape=set, size=.5)) 
ggtree(tree) # %<+% sets + geom_tiplab(size=4, offset=.3) + geom_tippoint(aes(color=set, shape=set, size=.5)) 
quit()
# p = p + geom_label(aes(label=node), fill='steelblue')
# p = p + geom_cladelabel(node=201, label="Mammalia", align=T, geom='label', offset=12)

png('animals_differences.png', width=1200, height=2000)
gheatmap(p, differences, width=.1, low="red", mid="white", high="blue", midpoint=0.0, use_scale_fill_gradient2=T, colnames=F, offset=5) 
dev.off()

png('animals_f1_scores.png', width=1200, height=2000)
gheatmap(p, f1_scores, width=.1, low="red", high="darkgreen", colnames=F, offset=5) 
dev.off()
