
library(cidr)

args <- commandArgs(trailingOnly=TRUE)

data_type <- args[1]
n_cluster <- args[2]
pc <- args[3]
large_data <- args[4]
data_path <- gsub("\\\\", "/", args[5])
pc_path <- gsub("\\\\", "/", args[6])
var_path <- gsub("\\\\", "/", args[7])

if (large_data == "False") {
  csv_data <- read.csv("stdin")
} else {
  csv_data <- read.csv(data_path)
}

data_object <- as.matrix(csv_data)

if (data_type == "cpm"){
  cidr_obj <- scDataConstructor(t(data_object), tagType = data_type)
} else {
    cidr_obj <- scDataConstructor(t(data_object))
} 

cidr_obj <- determineDropoutCandidates(cidr_obj)
cidr_obj <- wThreshold(cidr_obj)
cidr_obj <- scDissim(cidr_obj)
dissim_formatted <- format(cidr_obj@dissim, digits = 3, nsmall = 3)

pdf("cidr_plots.pdf")
cidr_obj <- scPCA(cidr_obj)

if (pc == 'True') {
  if (large_data == 'True') {
    write.csv(cidr_obj@PC, pc_path)
    write.csv(cidr_obj@variation, var_path)
  } else {
    write.csv(cidr_obj@PC, stdout())
    cat("---END OF PC---\n")
    write.csv(cidr_obj@variation, stdout())
  }
}

cidr_obj <- nPC(cidr_obj)

if (n_cluster != 'None') {
  #if there is an argument for the amount of clusters passed
  cidr_obj <- scCluster(cidr_obj, nCluster = as.integer(n_cluster))
} else {
  cidr_obj <- scCluster(cidr_obj)
}

plot(cidr_obj@PC[, c(1, 2)],
  col = cidr_obj@clusters,
  pch = cidr_obj@clusters,
  main = "CIDR Clustering",
  xlab = "PC1", ylab = "PC2"
)

