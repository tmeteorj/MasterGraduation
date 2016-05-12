dataread<-read.csv("plane/planeAllNormal.txt")
datadist=dist(dataread,method="euclidean")
hc=hclust(datadist,method="complete")
cut10=cutree(hc,k=10)
txt=data.frame(dataread$PID,cut10)
write.table(txt,file="cluster10.txt")

#dist:
#   manhattan
#   euclidean
#   minkowski
#   chebyshev
#   mahalanobis
#   canberra
#hclust:
#   average
#   centroid
#   median
#   complete    longest
#   single      nearest
#   ward
#   density
