library(ggplot2)
library(ggrepel)
library(gridExtra)

for (i in seq(0, 9, 1)){
  
  subpci <- pci
  subpci$split <- subpci[[paste0("split", i)]]
  bp12 <- ggplot(subpci, aes(x=PC2, y=PC1, shape=factor(pci$unrestricted), col=split)) +
            geom_point(size=3) +
            geom_text_repel(aes(label=species),  size=3) +
            scale_color_manual(values=c("grey40", "blue3", "black"), guide=FALSE) +
            scale_shape_manual(guide=FALSE, values=c(18, 16))
              
  bp13 <- ggplot(subpci, aes(x=PC3, y=PC1, shape=factor(pci$unrestricted), col=split)) +
            geom_point(size=3) +
            geom_text_repel(aes(label=species),  size=3) +
            scale_color_manual(values=c("grey40", "blue3", "black")) +
            scale_shape_manual(labels=c("yes", "no"),
                               values=c(18, 16), name="embargo restriction")
    
  joined <- grid.arrange(bp12, bp13, ncol=2)
  print(joined) 
  dev.copy2eps(file=paste0('plots/pca_split', i, '.eps'), width=20, height=12)
  dev.copy(png, file=paste0('plots/pca_split', i, '.png'), width=1200, height=800)
  dev.off()
}
