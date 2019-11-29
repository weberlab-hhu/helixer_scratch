args <- commandArgs(trailingOnly=TRUE)

basebam <- args[1]

introns <- read.csv(paste0(basebam, '.introns'), header=F)
uintrons <- read.csv(paste0(basebam, '.introns.uniq'), header=F)

big <- 1600
small <- 120
bigby <- big / 100
smallby <- small / 100

png(paste0(basebam,'_introns.png'), width=1200, height=800)
par(mfrow=c(2,2), mar=c(4.1,4.1,1.1,0.6))
hist(introns[,1], breaks=c(seq(0,big,bigby), Inf), xlim=c(0,big), col='grey40')
hist(introns[,1], breaks=c(seq(0,small,smallby), Inf), xlim=c(0,small), col='grey40')
hist(uintrons[,1], breaks=c(seq(0,big,bigby), Inf), xlim=c(0,big), col='grey40')
hist(uintrons[,1], breaks=c(seq(0,small,smallby), Inf), xlim=c(0,small), col='grey40')
dev.off()
