args <- commandArgs(trailingOnly=TRUE)
main_trials_dir <- args[1]
cov_file <- args[2]
out_dir <- args[3]

source('baseplot.R')

h=2.6
widths = c(6, 4)
widths = widths * 0.9
cex=0.54

targ_files <- c(cov_file, '/aug_vs_helixer.csv')
outdirs <- c(out_dir, 'plots/vs_aug/')
refs <- c('Ref', 'Aug')
rows_sc <- list(c(1:4, 9:10, 13:16),
                c(1, 3, 4, 9:10, 15:16))
rows_cov <- list(c(1:8, 13:16),
                 c(1, 3:4, 7:8, 15:16))
mwidths <- c(4, 3)
r_margin_cov <- c(2.1, 10.5) 
r_margin_cov[1] <- 2.6

pastepath <- function(...){
    paste(..., sep='/')
}

for (j in 1:1){
    targ_file <- targ_files[j]
    outdir <- outdirs[j]
    dir.create(outdir)
    ref <- refs[j]
    mw <- mwidths[j]
    w <- widths[j]
    source('import_nni.R')
    
    postscript(file=pastepath(outdir, 'averaged_spliced.eps'), height=h, width=w)
      par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, 10.1), cex=cex)
      ticksat <- viribp(summed_demelted_sc[rows_sc[[j]], ], 
                        ylab='average fraction of bp in\nspliced coverage bin',
                        ref=ref, match_length=mw)
      legend(ticksat[length(ticksat)] + 0.2, 1, rev(colnames(summed_demelted_sc)),
             fill=viridis(6), bty='n', title='Bin')
    dev.off()
    
    postscript(file=pastepath(outdir, 'averaged_coverage.eps'), height=h, width=w)
      par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, r_margin_cov[j]), cex=cex)
    
      ticksat <- viribp(summed_demelted_cov[rows_cov[[j]],],
                        ylab='average fraction of bp in\ncoverage bin',
                        ref=ref, match_length=mw)
    dev.off()
    
    for (sp in species){

        postscript(file=paste0(outdir, '/', sp, '_spliced.eps'), height=h, width=w)
          par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, 10.5), cex=cex)
          ticksat <- viribp(sp_demelted_sc[[sp]][rows_sc[[j]], ],
                            ylab='fraction of bp in\nspliced coverage bin',
                            ref=ref, match_length=mw)
          legend(ticksat[length(ticksat)] + 0.2, 1, rev(colnames(summed_demelted_sc)),
                 fill=viridis(6), bty='n', title='Bin')
        dev.off()
    
        postscript(file=paste0(outdir, '/', sp, '_coverage.eps'), height=h, width=w)
          par(xpd=TRUE, mar=c(5.1, 4.1, 4.1, r_margin_cov[j]), cex=cex)
    
          ticksat <- viribp(sp_demelted_cov[[sp]][rows_cov[[j]],],
                            ylab='fraction of bp in\ncoverage bin',
                            ref=ref, match_length=mw)
        dev.off()
    }
}
