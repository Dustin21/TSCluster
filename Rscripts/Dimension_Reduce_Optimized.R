# import dependencies
suppressPackageStartupMessages({
  require(tidyverse)
  require(e1071)
  require(plotly)
  require(Rtsne)
  require(largeVis)
  require(RColorBrewer)
  require(reshape2)
  require(ggplot2)
})

pfstat_boot <- function(x, nc, boot.n = 5, boot.p = 0.7, seed = 123)
  #****************************************************************
  # Bootstrap pseudo-fstatistic for range of clusters k using 
  # cmeans - Fuzzy c-means (FCM) is a method of clustering which 
  # allows one piece of data to belong to two or more clusters.
  # 
  # Inputs:
  #   x:      data set
  #   nc:     seq of clusters to iterate over
  #   boot.n: number of bootstrap samples
  #   boot.p: proportion of observations to sample on each boot
  #   seed:   seed to replicate results
  #
  # Return:
  #   stability plot of pseudo-F over each cluster assignment k
  #****************************************************************
{
  set.seed(seed)
  fstat <- NULL
  boots.mat <- matrix(NA, nrow = boot.n, ncol = length(nc))
  for(b in 1:boot.n)
  {
    boot <- dplyr::sample_n(x, boot.p * nrow(x))
    for(i in seq_along(nc))
    {
      clst <- e1071::cmeans(boot, centers = nc[i])$cluster
      boots.mat[b,i] <- clusterSim::index.G1(boot, clst)
    }
  }
  
  # boxplot
  boots.mat.df <- boots.mat
  colnames(boots.mat.df) <- nc
  boots.mat.plot <- data.frame(boots.mat.df) %>%
    reshape2::melt(variable.name = 'Cluster', value.name = 'Fstat', id.vars = NULL) %>%
    group_by(Cluster) %>%
    ggplot(aes(y = Fstat, x = Cluster)) +
    geom_point() + 
    geom_jitter(aes(colour = Cluster), alpha = 0.6) +
    geom_boxplot() +
    theme_bw()
  print(boots.mat.plot)
  
  # optimal cluster assignment
  clust.opt <- which.max(apply(boots.mat, 2, median)) + 1
  return(clust.opt)
}

dimReduction <- function(x, dim = 2)
  #****************************************************************
  # Perform largeVis TSNE mapping to 2 or 3 dimensional space. 
  # Ref: https://arxiv.org/abs/1602.00370
  # 
  # Inputs:
  #   x:   data set
  #   dim: dimension of map
  #
  # Return:
  #   coordinates of lower dimensional map
  #****************************************************************
{
  # drop index column
  dat <- dplyr::select(x, -id)
  
  # perform dim reduction
  embed_map <- largeVis::largeVis(t(dat), dim = dim)
  coords <- data.frame(t(embed_map$coords))
  
  return(coords)
}


#################################################################
########################### RUN SCRIPT ##########################
#################################################################

# import data
dat <- readr::read_csv("../outputs/clean_zNormalized_features.csv")

# perform dim reduction
coords <- dimReduction(dat, dim = 3)

# visualize pseudo f-stat and retrieve optimal k
opt.clst <- pfstat_boot(coords, nc = 2:5, boot.n = 50)

# get labels based on optimal results above
clst <- e1071::cmeans(coords, centers = 13)

# plot results
plotly::plot_ly(data = data.frame(coords), 
                x = ~X1, y = ~X2, type="scatter", mode = "markers" , 
                 marker = list(size = 1))
#color = ~as.factor(labels),

write_csv(coords, "../outputs/z_mapped_3d.csv")

library(scatterplot3d)
scatterplot3d(x = coords[,1], y = coords[,2], z = coords[,3], pch=".", 
              cex.symbols=0.1, angle = 180)
