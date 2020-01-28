library(grid)
library(ggplot2)
library(gridExtra)


expl_cov <- function(x){
  n <- length(x)
  out <- paste('[', x[1:(n - 1)], ', ', x[2:n], ')', sep='')
  out <- c(out, paste0(x[n], '+'))
  return(out)
}

cm_labs <- function(x, decode){
  #if (x[1] == 0 & x[2] == 0){
  #  return('R: ig   \nP: ig   ')
  #}else{
    return(paste(decode[x + 1], collapse='\n'))
  #}
}

estimate_y_labs <- function(bp){
  builtthing <- ggplot_build(bp)
  arange <- builtthing$layout$panel_params[[1]]$y.range
  adist <- arange[2] - arange[1]
  print(arange)
  # 10% below axis?
  return(arange[1] - adist * 0.1)
}

ypos <- -0.2
paircov_plot <- function(cov, 
			 argmax0=0, 
			 argmax1=1, 
			 covstring="coverage_greater_eq",
			 position="fill"){
  decode = c("ig", "UTR", "CDS", "intron")
  argmaxes <- c(argmax0, argmax1)
  x <- cov[cov$argmax_y %in% argmaxes & cov$argmax_pred  %in% argmaxes, ]
  x$ref_pred = apply(x[, c('argmax_y', 'argmax_pred')], 1, cm_labs, decode=decode)
  x$ref_pred = factor(x$ref_pred, levels=unique(x$ref_pred))
  cov_bin <- factor(x[, covstring], 
			levels=sort(unique(x[, covstring])))
  levels(cov_bin) <- expl_cov(levels(cov_bin))
  x$cov_bin <- cov_bin
  if (position == "fill"){
    ylab_str = "fraction of positions"
  }else{
    ylab_str = "count of positions"
  }
  #x <- rbind(x, c(NA, NA, NA, NA, NA, 'ref.\npred.', NA))
  bp <- ggplot(x, aes(x=ref_pred, y=count, fill=cov_bin)) +
	  geom_bar(stat='identity', position=position) + 
          scale_fill_viridis_d(direction=1) +
	  ylab(ylab_str) +
          xlab("") 
#
#	  ggtitle(paste0(argmax0, " = ", decode[argmax0 + 1], 
#			 ", ", argmax1, " = ", decode[argmax1 + 1],
#			 "\n", covstring))
  ypos <- estimate_y_labs(bp)
  print(ypos)
  bp <- bp + annotation_custom(textGrob(" Ref.:\nPred.:"), 
            xmin=0, xmax=0,ymin=ypos, ymax=ypos) +
        scale_x_discrete(labels=c('\n', '\n', '\n', '\n')) + 
        theme(plot.margin=unit(c(8, 8, 24, 16), "pt"))
#        theme(axis.text.x=element_blank())
  for (i in 1:4){
          bp <- bp + annotation_custom(textGrob(levels(x$ref_pred)[i]), 
            xmin=i, xmax=i,ymin=ypos, ymax=ypos)
  }
  
  g = ggplotGrob(bp)
  g$layout$clip[g$layout$name=="panel"] <- "off"
  #grid.draw(g)
  return(g)
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
