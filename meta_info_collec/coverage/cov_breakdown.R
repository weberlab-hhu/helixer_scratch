library(ggplot2)
library(gridExtra)

paircov_plot <- function(x, 
			 argmax0=0, 
			 argmax1=1, 
			 covstring="coverage_greater_eq",
			 position="fill"){
  decode = c("intergenic", "UTR", "CDS", "intron")
  argmaxes <- c(argmax0, argmax1)
  x <- cov[cov$argmax_y %in% argmaxes & cov$argmax_pred  %in% argmaxes, ]
  x$ref_pred = apply(x[, c('argmax_y', 'argmax_pred')], 1,paste, collapse=':')
  cov_bin <- factor(x[, covstring], 
			levels=sort(unique(x[, covstring]), decreasing=T))
  x$cov_bin <- cov_bin
  if (position == "fill"){
    ylab_str = "fraction of positions"
  }else{
    ylab_str = "count of positions"
  }
  bp <- ggplot(x, aes(x=ref_pred, y=count, fill=cov_bin)) +
	  geom_bar(stat='identity', position=position) + 
          scale_fill_viridis_d(direction=-1) +
	  xlab("reference:prediction") +
	  ylab(ylab_str) +
	  ggtitle(paste0(argmax0, " = ", decode[argmax0 + 1], 
			 ", ", argmax1, " = ", decode[argmax1 + 1],
			 "\n", covstring))
  return(bp)
}

fullpair4 <- function(x,
                       argmax0=0,
                       argmax1=1){
  cov_rel <- paircov_plot(x, argmax0, argmax1, "coverage_greater_eq")
  scov_rel <- paircov_plot(x, argmax0, argmax1, "spliced_coverage_greater_eq")
  cov_abs <- paircov_plot(x, argmax0, argmax1, "coverage_greater_eq", position="stack")
  scov_abs <- paircov_plot(x, argmax0, argmax1, "spliced_coverage_greater_eq", position="stack")
  return(grid.arrange(cov_rel, scov_rel, cov_abs, scov_abs, nrow=2, ncol=2))
}
