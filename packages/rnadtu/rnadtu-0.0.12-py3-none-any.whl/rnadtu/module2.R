print("1")

library(cidr)


args <- commandArgs(trailingOnly=TRUE)

print(paste0(
  "Your chosen arguments are: ",
  "tagType: ", args[1], ", ",
  "nCluster: ", args[2]
))

print(paste("args[1] is:", args[1]))

csv_data <- read.csv("annDataToCSV.csv")
data_object <- as.matrix(csv_data)

if (args[1] == "cpm"){
  cidr_obj <- scDataConstructor(t(data_object), tagType="cpm")
} else {
    cidr_obj <- scDataConstructor(t(data_object))
} 

print(cidr_obj@tagType)

print("object created")

cidr_obj <- determineDropoutCandidates(cidr_obj)

print("determined dropout candidates")

cidr_obj <- wThreshold(cidr_obj)

print("determined thresholds")


cidr_obj <- scDissim(cidr_obj)

print("created dissimilaity matrix")

dissim_formatted <- format(cidr_obj@dissim, digits = 3, nsmall = 3)



cidr_obj <- scPCA(cidr_obj)

print("PCA done")

cidr_obj <- nPC(cidr_obj)

print("nPC done")


if (args[2] != 'None') {
  #if there is an argument for the amount of clusters passed
  cidr_obj <- scCluster(cidr_obj, nCluster=as.integer(args[2]))
} else {
  cidr_obj <- scCluster(cidr_obj)
}



print("cluster done")

plot(cidr_obj@PC[, c(1, 2)],
  col = cidr_obj@clusters,
  pch = cidr_obj@clusters,
  main = "CIDR Clustering",
  xlab = "PC1", ylab = "PC2"
)

print("plot done")

