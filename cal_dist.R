library(data.table)
library(ggplot2)
library(ggExtra)
# This is the file we generated: /data1/Human/ibdmdb2/metatranscriptomics/CSM79HGP_MGX.vs.MTX
df = fread("/Users/odedsabah/Desktop/CSM79HGP.coverages.10x.txt")
# --- Density plot for contigs coverage area
png('~/Downloads/Density_hist.png')
p = ggplot(df, aes(V4, V5)) +  geom_point(alpha = 0.2) + geom_smooth(method = lm) +
  xlim(0,100) + xlab("Start coverage") +
  ylim(0,100) + ylab("End coverage") +
  geom_rug(col=rgb(0,0,0.6,alpha=0.2))
ggMarginal(p, type = "histogram")
dev.off()