# read in table
x <- read.csv('tables/Tcacao/cov_scores.csv', row.names=1)

# collapse out Augustus (for now, later option of 3)
hm <- rownames(x)
hmf <- factor(gsub(', [0-3])', ')', hm))
x2 <- t(sapply(split(x, hmf), colSums))

# calculate quantiles

bins <- colnames(x2)
bins <- as.numeric(gsub('X', '', bins))

quant_frm_hist <- function(xhist, bins, quantiles){
    cs <- cumsum(as.vector(xhist))
    out <- c()
    for (q in quantiles){
        out <- c(out, which(cs > cs[length(cs)] * q)[1])
    }
    return(bins[out])
}

targ_quantiles <- c(0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9)
xq <- t(apply(x2, 1, quant_frm_hist, bins=bins, quantiles=targ_quantiles))
colnames(xq) <- paste0('q', targ_quantiles)

o <- c('(0, 0)',
       '(1, 1)',
       '(2, 2)',
       '(3, 3)',
       '(0, 1)',
       '(1, 0)',
       '(0, 2)',
       '(2, 0)',
       '(0, 3)',
       '(3, 0)',
       '(1, 2)',
       '(2, 1)',
       '(1, 3)',
       '(3, 1)',
       '(2, 3)',
       '(3, 2)')

x3 <- sapply(seq(1,1000,50), function(i) rowMeans(x2[,i:(i + 49)]))
x3 <- x3[o,]
par(mfrow=c(7,1), mar=c(1,1,0.5,0.5))
i <- 3
mycols <- c('red3', 'green3', 'blue3','gold2')
plot(cumsum(x3[i,])/sum(x3[i,]), type='l', col=mycols[i])
for (i in c(1,2,4)){
  lines(cumsum(x3[i,])/sum(x3[i,]), type='l', col=mycols[i])
}
legend('bottomright', legend=rownames(x3)[1:4], col=mycols, lty=1)

for (i in seq(5,16,2)){
  plot(cumsum(x3[i,])/sum(x3[i,]), type='l')
  lines(cumsum(x3[i + 1,])/sum(x3[i + 1,]), lty=2)
  legend('bottomright', legend=rownames(x3)[i:(i+1)], lty=c(1,2))
}
