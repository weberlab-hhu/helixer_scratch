# need a couple helper functions from this one
source('cov_breakdown.R')

sum_list_elements <- function(x){
    out <- x[[1]]
    for (i in 2:length(x)){
        out <- out + x[[i]]
    }
    return(out)
}

mk_covbin <- function(x, covstring){
    cov_bin <- factor(x[, covstring],
                      levels=sort(unique(x[, covstring])))
    levels(cov_bin) <- expl_cov(levels(cov_bin))
    return(cov_bin)
}

# go from multi factor format to 2D table 
sum_ref_pred <- function(x) {
    sapply(split(x, x$ref_pred), function(w) sum(w$count))
}

unmelt <- function(x, cov_col){
    # x has to be a table as created by coverage_counter.py, 
    # but with the two 'argmax' columns combined to 'ref_pred'
    demelt <- sapply(split(x, x[, cov_col]), sum_ref_pred)
    demelt <- demelt[,ncol(demelt):1]
    demelt <- demelt / rowSums(demelt)
    return(demelt)
}

decode = c("IG", "UTR", "CDS", "Ntrn")

## go from 
species <- list.files('pairwise/')
sp_list <- lapply(species, function(x) read.csv(paste0('pairwise/', x, targ_file)))
# setup refernce vs prediction descriptive names
for (i in 1:length(sp_list)){
    sp_list[[i]]$ref_pred <- apply(sp_list[[i]][, c('argmax_y', 'argmax_pred')], 1, cm_labs, decode=decode)
    sp_list[[i]]$ref_pred <- factor(sp_list[[i]]$ref_pred, levels=unique(sp_list[[i]]$ref_pred))
    sp_list[[i]]$cov_bin  <- mk_covbin(sp_list[[i]], 'coverage_greater_eq')
    sp_list[[i]]$sc_bin  <- mk_covbin(sp_list[[i]], 'spliced_coverage_greater_eq')
}
names(sp_list) <- species

sp_demelted_cov <- lapply(sp_list, unmelt, cov_col='cov_bin')
# convenience reorder
sp_demelted_cov <- lapply(sp_demelted_cov, function(x) x[c(1,6,11,16, 2,5,3,9,4,13,7,10,8,14,12,15),])
summed_demelted_cov <- sum_list_elements(sp_demelted_cov) / length(sp_demelted_cov)
sp_demelted_sc <- lapply(sp_list, unmelt, cov_col='sc_bin')
# convenience reorder
sp_demelted_sc <- lapply(sp_demelted_sc, function(x) x[c(1,6,11,16, 2,5,3,9,4,13,7,10,8,14,12,15),])
summed_demelted_sc <- sum_list_elements(sp_demelted_sc) / length(sp_demelted_sc)

