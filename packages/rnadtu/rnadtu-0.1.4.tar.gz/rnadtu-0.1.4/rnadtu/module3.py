from scipy.sparse import csr_matrix
from module1 import sparse_to_csv
import os



def cidr_rpy2(a_data, layer=None, data_type="raw", n_cluster=None, pc=False, save_clusters=True):
    # Runs CIDR algorithm with rpy2.
    # The lines that start with ro.r is a way of running R-code in python.

    # Import of rpy2 is set here instead on top of module, making it possible to import the package
    # without needing to install rpy2, since this package might not always compile in a windows environment.
    try:
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        from rpy2.robjects import r
        from rpy2.robjects import globalenv
        from rpy2.robjects.packages import importr
    except ImportError:
        raise ImportError("rpy2 must be installed to use 'cidr_rpy2'")

    # Imports the CIDR package installed in R.
    cidr = importr("cidr")

    # Chooses data, save it as a data_object through a few computations.
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    sparse_to_csv(sparse_matrix, 'anndata_to_csv.csv')
    ro.r('csv_data <- read.csv("anndata_to_csv.csv")')
    ro.r('data_object <- as.matrix(csv_data)')
    # Runs CIDR on data_object.
    ro.globalenv['data_type'] = data_type
    ro.r('''if (data_type == "cpm"){
            cidr_obj <- scDataConstructor(t(data_object), tagType="cpm")
            } else {
            cidr_obj <- scDataConstructor(t(data_object))
            }''')
    print("Object created (1/8)")
    ro.r('cidr_obj <- determineDropoutCandidates(cidr_obj)')
    print("Determined dropout candidates (2/8)")
    ro.r('cidr_obj <- wThreshold(cidr_obj)')
    print("Determined threshold (3/8)")
    ro.r('cidr_obj <- scDissim(cidr_obj)')
    print("Created dissimilaity matrix (4/8)")
    ro.r('pdf("cidr_plots.pdf")')
    ro.r('cidr_obj <- scPCA(cidr_obj)')
    print("Finished principal component analysis (5/8)")
    ro.r('cidr_obj <- nPC(cidr_obj)')
    print("Determined number of principal components (6/8)")

    # If n_cluster, then it chooses n_cluster as amount of clusters, otherwise
    # choosing best fitting amount.
    if n_cluster == None:
        ro.r('cidr_obj <- scCluster(cidr_obj)')
    else:
        ro.globalenv['n_cluster'] = n_cluster
        ro.r('cidr_obj <- scCluster(cidr_obj, nCluster=as.integer(n_cluster))')

    print("Finished clustering (7/8)")
    ro.r('''

    plot(cidr_obj@PC[, c(1, 2)],
      col = cidr_obj@clusters,
      pch = cidr_obj@clusters,
      main = "CIDR Clustering",
      xlab = "PC1", ylab = "PC2"
    )
    dev.off()
    ''')
    print("Plot done (8/8)")

    # If save_clusters, then the clusters are saved in the a_data object.
    if save_clusters == True:
        clusters = ro.r('as.data.frame(cidr_obj@clusters)')
        from rpy2.robjects.conversion import localconverter
        from rpy2.robjects import default_converter
        with localconverter(default_converter + pandas2ri.converter):
            clusters_df = ro.conversion.rpy2py(clusters)

        # Chooses the layer in which you save the clusters.
        if layer == None:
            a_data.obsm['X_cidr_clusters'] = clusters_df.values
        else:
            a_data.obsm[layer + '_cidr_clusters'] = clusters_df.values

    # If pc true in cidr function, then principal coordinates it put in a_data object.
    if pc == True:
        pcs = ro.r('as.data.frame(cidr_obj@PC)')
        variation = ro.r('as.data.frame(cidr_obj@PC)')

        from rpy2.robjects.conversion import localconverter
        from rpy2.robjects import default_converter

        with localconverter(default_converter + pandas2ri.converter):
            pcs_df = ro.conversion.rpy2py(pcs)
            variation_df = ro.conversion.rpy2py(variation)

        # Chooses the layer in which you save the principal coordinates.
        if layer == None:
            a_data.obsm['X_cidr_pca'] = pcs_df.values
            a_data.uns['X_variation'] = variation_df

        else:
            a_data.obsm[layer + '_cidr_pca'] = pcs_df.values
            a_data.uns[layer + '_variation'] = variation_df

        print("Algorithm done. Plots are in cidr_plots.pdf")
    return a_data
