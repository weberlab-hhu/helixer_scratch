args <- commandArgs(trailingOnly=TRUE)

cov_file <- args[1]
file_out <- args[2]

print(cov_file)
print(file_out)

# check file endings for sanity
will_stop <- FALSE
if (length(grep('.csv', file_out)) > 0){
  will_stop <- TRUE
}else if(! length(grep('.csv', cov_file)) > 0){
  will_stop <- TRUE
}else if(length(grep('.eps', cov_file)) > 0){
  will_stop <- TRUE
}else if(! length(grep('.eps', file_out)) > 0){
  will_stop <- TRUE
}
if (will_stop){
  stop("arguments must be: INPUT.csv OUTPUT.eps")
}
source('cov_breakdown.R')

cov <- read.csv(cov_file)

postscript(file_out)
for (i in 0:2){
  for (j in (i + 1):3){
    fullpair4(cov, i, j)
  }
}
dev.off()
