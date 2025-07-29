# # Implementing the CIDR function with rpy2.

def cidr_rpy2(a_data, layer=None, data_type = "raw", n_cluster=None, pc = False, save_clusters = True):
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
    from .module1 import sparse_to_csv
    # Choose layer X if no other is specified
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    sparse_to_csv(sparse_matrix, 'anndata_to_csv.csv')
    ro.r('csv_data <- read.csv("anndata_to_csv.csv")')
    ro.r('data_object <- as.matrix(csv_data)')

    ro.globalenv['data_type'] = data_type
    ro.r('''if (data_type == "cpm"){
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
    ro.r('pdf("cidr_plots.pdf")')
    ro.r('cidr_obj <- scPCA(cidr_obj)')
    ro.r('print("PCA done")')
    ro.r('cidr_obj <- nPC(cidr_obj)')
    ro.r('print("nPC done")')

    if n_cluster == None:
        ro.r('cidr_obj <- scCluster(cidr_obj)')
    else:
      ro.globalenv['n_cluster'] = n_cluster
      ro.r('cidr_obj <- scCluster(cidr_obj, nCluster=as.integer(n_cluster))')

    ro.r('print("cluster done")')
    ro.r('''

    plot(cidr_obj@PC[, c(1, 2)],
      col = cidr_obj@clusters,
      pch = cidr_obj@clusters,
      main = "CIDR Clustering",
      xlab = "PC1", ylab = "PC2"
    )
    dev.off()
    ''')
    ro.r('print("plot done")')
    if save_clusters == True:
      clusters = ro.r('as.data.frame(cidr_obj@clusters)')
      from rpy2.robjects.conversion import localconverter
      from rpy2.robjects import default_converter
      with localconverter(default_converter + pandas2ri.converter):
        clusters_df = ro.conversion.rpy2py(clusters)
      if layer == None:
        a_data.obsm['X_cidr_clusters'] = clusters_df.values
      else :
        a_data.obsm[layer + '_cidr_clusters'] = clusters_df.values

    if pc == True:
      pcs = ro.r('as.data.frame(cidr_obj@PC)')
      variation = ro.r('as.data.frame(cidr_obj@PC)')

      from rpy2.robjects.conversion import localconverter
      from rpy2.robjects import default_converter

      with localconverter(default_converter + pandas2ri.converter):
        pcs_df = ro.conversion.rpy2py(pcs)
        variation_df = ro.conversion.rpy2py(variation)

      if layer == None:
        a_data.obsm['X_cidr_pca'] = pcs_df.values
        a_data.uns['X_variation'] = variation_df

      else:
        a_data.obsm[layer + '_cidr_pca'] = pcs_df.values
        a_data.uns[layer + '_variation'] = variation_df

      print("Algorithm done. Plots are in cidr_plots.pdf")
    return a_data
