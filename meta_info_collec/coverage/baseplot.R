library(viridis)

viribp <- function(demelt, ylab='fraction of bp with\ncoverage in bin', ref='Ref', match_length=4){

    n_pairwise <- (nrow(demelt) - match_length) / 2
    exon_widths <- c(0.0, 0.3)[c(rep(1, match_length), rep(c(2,1), n_pairwise))]

    padj = 0.7
    xat <- barplot(t(demelt), col=rev(viridis(6)), space=exon_widths, padj=padj)
    title(ylab=ylab, line=1.7, cex=1.2)
    ticksat <- unique(c(xat - 0.5, xat + 0.5))
    ticksat <- sort(ticksat)
    before_pairs <- match_length + 1
    axis(1, at=ticksat[1:before_pairs], labels=rep('', before_pairs))
    for (i in seq(1, n_pairwise * 3, 3)){
        axis(1, at=ticksat[0:2 + i + before_pairs], labels=rep('', 3))
    }
    axis(1, at=-.5, labels=paste0('     ', ref, '.:   \nHelixer:   '), tick=F, padj=padj)
    return(ticksat)
}

