


library(cidr)

args <- commandArgs(trailingOnly=TRUE)

data_type <- args[1]
n_cluster <- args[2]
pc <- args[3]
drop_cand <- args[4]
large_data <- args[5]
data_path <- gsub("\\\\", "/", args[6])
pc_path <- gsub("\\\\", "/", args[7])
var_path <- gsub("\\\\", "/", args[8])
drop_cand_path <- gsub("\\\\", "/", args[9])

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

cat("Object created (1/8)\n", file = stderr())

cidr_obj <- determineDropoutCandidates(cidr_obj)

if (drop_cand == 'True') {
    if (large_data == 'True') {
      write.csv(cidr_obj@dropoutCandidates, drop_cand_path)
  } else {
    write.csv(cidr_obj@dropoutCandidates, stdout())
    cat("---END OF DROPOUT CANDIDATES---\n")
  }
}

cat("Determined dropout candidates (2/8)\n", file = stderr())

cidr_obj <- wThreshold(cidr_obj)

cat("Determined threshold (3/8)\n", file = stderr())


cidr_obj <- scDissim(cidr_obj)
cat("Created dissimilarity matrix (4/8)\n", file = stderr())

pdf("cidr_plots.pdf")
cidr_obj <- scPCA(cidr_obj)

cat("Finished principal component analysis (5/8)\n", file = stderr())

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

cat("Determined number of principal components (6/8)\n", file = stderr())

if (n_cluster != 'None') {
  #if there is an argument for the amount of clusters passed
  cidr_obj <- scCluster(cidr_obj, nCluster = as.integer(n_cluster))
} else {
  nCluster(cidr_obj)
  cidr_obj <- scCluster(cidr_obj)
}

cat("Finished clustering (7/8)\n", file = stderr())

plot(cidr_obj@PC[, c(1, 2)],
  col = cidr_obj@clusters,
  pch = cidr_obj@clusters,
  main = "CIDR Clustering",
  xlab = "PC1", ylab = "PC2"
)

cat("Plot done (8/8)\n", file = stderr())