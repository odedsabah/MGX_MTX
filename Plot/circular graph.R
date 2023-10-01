
#---
#title: "Create graphs for figure 1 to thesis"
#date: "4/5/2022"
#input:  coverage Statistics of CSM79HGP.MGX
#output:A circular graph showing the data distribution of samples from IBDMDB
#---

# Upload packages

library(ggplot2)
library(hrbrthemes)
library(dplyr)
library(tidyr)
library(viridis)


## input data table

CSM79HGP_MGX <- read.table("/Users/odedsabah/Desktop/CSM79HGP.MGX.coverage-stats.txt")

CSM79HGP_MTX <- read.table("/Users/odedsabah/Desktop/CSM79HGP.MTX.coverage-stats.txt")

# clacolate retio between mean - median

mean_MGX <- as.double(CSM79HGP_MGX$V5)
median_MGX <- as.double(CSM79HGP_MGX$V4)
Division_Mea_Med_MGX <- mean_MGX/median_MGX


hist(mean_MGX)
hist(median_MGX)
hist(Division_Mea_Med_MGX)
plot(Division_Mea_Med_MGX)


mean_MTX <- as.double(CSM79HGP_MTX$V5)
median_MTX <- as.double(CSM79HGP_MTX$V4)
Division_Mea_Med_MTX <- mean_MTX[median_MTX != 0 ]/median_MTX[median_MTX != 0 ]
vec = (Division_Mea_Med_MTX[complete.cases(Division_Mea_Med_MTX)])
plot(vec, ylim = c(0,10))


hist(mean_MTX)
hist(median_MTX)

# combin the columes to df
com_vec <- cbind(Division_Mea_Med_MGX,Division_Mea_Med_MTX)
com2df = as.data.frame(com_vec)

set.seed(1)
c2c1 <- pivot_longer(com2df,Division_Mea_Med_MGX:Division_Mea_Med_MTX)
c2c1

# Represent the Relationship distribution
png('~/Downloads/x.png')
c2c1 %>%
  ggplot( aes(x=value, fill=name)) +
    geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity') +
    scale_fill_manual(values=c("#69b3a2", "#404080")) +
    theme_ipsum() +
    xlim(c(0.5,2)) +
    labs(x="Ratio between average and median", y="frequency") +
    theme_minimal() +
    theme(legend.position = "none") +
    theme(panel.background = element_blank())
dev.off()


set.seed(125)
# sample <- read.csv("/Users/odedsabah/Desktop/Book5 2.csv")
sample <- read.csv("/Users/odedsabah/Downloads/To_circularplot.csv")

sample<- as.matrix(sample)
rownames(sample) <- c("CD","IBD", "nonIBD","UC")

library(circlize)
circos.par(gap.degree = 4)
chordDiagram(sample, directional = TRUE, annotationTrack = "grap",
  preAllocateTracks = list(list(track.height = 0.05),
                           list(track.height = 0.05)))
circos.trackPlotRegion(track.index = 1, panel.fun = function(x, y) {
  xlim = get.cell.meta.data("xlim")
  ylim = get.cell.meta.data("ylim")
  sector.index = get.cell.meta.data("sector.index")
  circos.text(mean(xlim), mean(ylim), sector.index, facing = "inside", niceFacing = TRUE)
}, bg.border = NA)
circos.trackPlotRegion(track.index = 2, panel.fun = function(x, y) {
  circos.axis("bottom", major.tick.percentage = 0.2, labels.cex = 0.4)
}, bg.border = NA, bg.col = NA)
circos.clear()

