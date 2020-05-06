h=2.6
widths = c(6, 4)
cex=0.55

targ_files <- c('/ref_vs_helixer.csv', '/aug_vs_helixer.csv')
outdirs <- c('plots/vs_ref/', 'plots/vs_aug/')
refs <- c('Ref', 'Aug')
rows_sc <- list(c(1:4, 9:10, 13:16),
                c(1, 3, 4, 9:10, 15:16))
rows_cov <- list(c(1:8, 13:16),
                 c(1, 3:4, 7:8, 15:16))
mwidths <- c(4, 3)
r_margin_cov <- c(2.1, 10.5) 

for (j in 1:2){
    targ_file <- targ_files[j]
    outdir <- outdirs[j]
    ref <- refs[j]
    mw <- mwidths[j]
    w <- widths[j]
    source('import.R')
    
    postscript(file=paste0(outdir, 'averaged_spliced.eps'), height=h, width=w)
      par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, 10.5), cex=cex)
      ticksat <- viribp(summed_demelted_sc[rows_sc[[j]], ], 
                        ylab='average fraction of bp in\nspliced coverage bin',
                        ref=ref, match_length=mw)
      legend(ticksat[length(ticksat)] + 0.2, 1, colnames(summed_demelted_sc),
             fill=viridis(6), bty='n', title='Bin')
    dev.off()
    
    postscript(file=paste0(outdir, 'averaged_coverage.eps'), height=h, width=w)
      par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, r_margin_cov[j]), cex=cex)
    
      ticksat <- viribp(summed_demelted_cov[rows_cov[[j]],],
                        ylab='average fraction of bp in\ncoverage bin',
                        ref=ref, match_length=mw)
    dev.off()
    
    for (sp in species){

        postscript(file=paste0(outdir, sp, '_spliced.eps'), height=h, width=w)
          par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, 10.5), cex=cex)
          ticksat <- viribp(sp_demelted_sc[[sp]][rows_sc[[j]], ],
                            ylab='average fraction of bp in\nspliced coverage bin',
                            ref=ref, match_length=mw)
          legend(ticksat[length(ticksat)] + 0.2, 1, colnames(summed_demelted_sc),
                 fill=viridis(6), bty='n', title='Bin')
        dev.off()
    
        postscript(file=paste0(outdir, sp, '_coverage.eps'), height=h, width=w)
          par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, r_margin_cov[j]), cex=cex)
    
          ticksat <- viribp(sp_demelted_cov[[sp]][rows_cov[[j]],],
                            ylab='average fraction of bp in\ncoverage bin',
                            ref=ref, match_length=mw)
        dev.off()
    }
}
