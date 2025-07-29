import anndata as ad  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from scipy.sparse import csr_matrix  # type: ignore
import subprocess
import os

# # Get current working directory
# current_path = os.getcwd()

# # Build a new path by appending a folder name
# new_path = os.path.join(current_path, "FinalPackage", "rnadtu")

# # Change into that directory
# os.chdir(new_path)

# print(os.getcwd())


def sparseToCsv(sparseMatrix, csvName):

    # Convert sparse matrix to an array
    arrayMatrix = sparseMatrix.toarray()

    # Convert array to a DataFrame
    df = pd.DataFrame(arrayMatrix)

    # Export to csv
    df.to_csv(f'{csvName}.csv', index=False)




def makeArgs(dataType, nCluster):
    args = [None] * 4
    args[0] = "Rscript"

    # Get path to module2.R (same folder as this file)
    r_script_path = os.path.join(os.path.dirname(__file__), "module2.R")
    args[1] = r_script_path

    args[2] = str(dataType)
    args[3] = str(nCluster)
    return args


def cidr(aData, layer=None, dataType = "raw", nCluster=None):
    print("Algorithm Starting...")
    # Does CIDR on adata.X if no layer specified.
    data = aData.X if layer is None else aData.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    sparseToCsv(sparse_matrix, 'annDataToCSV')
    print(subprocess.run(makeArgs(dataType, nCluster), check=True).stderr)


# annD = ad.io.read_csv("symsim_observed_counts_5000genes_1000cells_complex.csv",
#                       delimiter=',', first_column_names=None, dtype='float32')
    

# cidr(annD)

