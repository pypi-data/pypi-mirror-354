


# # Implementing the CIDR function with rpy2.

# print(os.getcwd())

# # Get current working directory
# current_path = os.getcwd()

# # Build a new path by appending a folder name
# new_path = os.path.join(current_path, "rnadtu")

# # Change into that directory
# os.chdir(new_path)


def cidr_rpy2(aData, layer=None, dataType = "raw", nCluster=None):
    import os
    try:
      import rpy2.robjects as ro
      from rpy2.robjects import pandas2ri
      from rpy2.robjects import r
      from rpy2.robjects import globalenv
    except ImportError:
      raise ImportError("rpy2 must be installed to use 'cidr_rpy2'")
    import anndata as ad
    import numpy as np
    import pandas as pd


    from scipy.sparse import csr_matrix
    # Function from rpy2 that makes it possible to use other R-packages directly in python.
    try:
      from rpy2.robjects.packages import importr
    except ImportError:
      raise ImportError("rpy2 must be installed to use 'cidr_rpy2'")
    # Imports the CIDR package installed in R.
    cidr = importr("cidr")
    from .module1 import sparseToCsv
    #choose layer X if no other is specified
    data = aData.X if layer is None else aData.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    sparseToCsv(sparse_matrix, 'annDataToCSV')
    ro.r('csv_data <- read.csv("annDataToCSV.csv")')
    ro.r('data_object <- as.matrix(csv_data)')
    
    ro.globalenv['dataType'] = dataType
    ro.r('''if (dataType == "cpm"){
            cidr_obj <- scDataConstructor(t(data_object), tagType="cpm")
            } else {
            cidr_obj <- scDataConstructor(t(data_object))
            }''') 
    ro.r('print("object created")')
    ro.r('cidr_obj <- determineDropoutCandidates(cidr_obj)')
    ro.r('print("determined dropout candidates")')
    ro.r('cidr_obj <- wThreshold(cidr_obj)')
    ro.r('print("determined thresholds")')
    ro.r('cidr_obj <- scDissim(cidr_obj)')
    ro.r('print("created dissimilaity matrix")')
    ro.r('dissim_formatted <- format(cidr_obj@dissim, digits = 3, nsmall = 3)')
    ro.r('write.csv(t(dissim_formatted), "dissimMatrix.csv")')
    ro.r('cidr_obj <- scPCA(cidr_obj)')
    ro.r('print("PCA done")')
    ro.r('cidr_obj <- nPC(cidr_obj)')
    ro.r('print("nPC done")')
    
    if nCluster == None:
        ro.r('cidr_obj <- scCluster(cidr_obj)')
    else:
      ro.globalenv['nCluster'] = nCluster
      ro.r('cidr_obj <- scCluster(cidr_obj, nCluster=as.integer(nCluster))')

    ro.r('print("cluster done")')
    ro.r('''
    png("cidr_plot.png")
    plot(cidr_obj@PC[, c(1, 2)],
      col = cidr_obj@clusters,
      pch = cidr_obj@clusters,
      main = "CIDR Clustering",
      xlab = "PC1", ylab = "PC2"
    )
    dev.off()
    ''')
    ro.r('print("plot done")')


