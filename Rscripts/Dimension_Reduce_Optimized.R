# import dependencies
suppressPackageStartupMessages({
  require(tidyverse)
  require(e1071)
  require(plotly)
  require(Rtsne)
  require(largeVis)
  require(RColorBrewer)
  require(diceR)
})

pfstat_boot <- function(x, nc, boot.n = 5, boot.p = 0.7, seed = 123)
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
  boxplot(boots.mat, names = nc)
}


# import data
dat <- readr::read_csv("../outputs/clean_zNormalized_features.csv")

# perform dim reduction
embed_map <- largeVis::largeVis(t(dat[,-1]), dim = 2)
coords <- data.frame(t(embed_map$coords))

# visualize pseudo f-stat and retrieve optimal k
opt.clst <- pfstat_boot(coords, nc = 4:20, boot.n = 50)

# get labels based on optimal results above
clst <- e1071::cmeans(coords, centers = 13)

# plot results
plotly::plot_ly(data = data.frame(labels = clst$cluster, coords), 
                x = ~X1, y = ~X2, type="scatter", mode = "markers" , 
                 marker = list(size = 1))
#color = ~as.factor(labels),


library(scatterplot3d)
scatterplot3d(x = out2[,1], y = out2[,2], z = out2[,3], pch=".", 
              cex.symbols=0.1, angle = 300)