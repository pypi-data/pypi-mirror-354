import anndata as ad  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from scipy.sparse import csr_matrix  # type: ignore
import subprocess
import os
import tempfile
from io import StringIO

def sparse_to_csv(sparse_matrix, csv_name):
    # Save a sparse matrix as a csv file
    array_matrix = sparse_matrix.toarray()
    df = pd.DataFrame(array_matrix)
    df.to_csv(csv_name, index=False)

def sparse_to_csv_using_buffer(sparse_matrix):
    from io import StringIO
    array_matrix = sparse_matrix.toarray()
    df = pd.DataFrame(array_matrix)
    # makes the buffer for an input stream
    in_ram = StringIO()
    df.to_csv(in_ram, index=False)
    return in_ram.getvalue()

def make_args(data_type, n_cluster, pc, large, file_path = None, pc_path = None, var_path= None):
    # Make an argumentlist to the R-script."
    script_path = os.path.join(os.path.dirname(__file__), "module2.R")
    
    return ["Rscript",
            script_path,
            str(data_type),
            str(n_cluster),
            str(pc),
            str(large),
            str(file_path),
            str(pc_path),
            str(var_path)]

def handle_pc(a_data, layer, pc_path, var_path):
    pc = pd.read_csv(pc_path, index_col=0)
    pc_array = pc.to_numpy()
    variation = pd.read_csv(var_path, index_col=0)
    variation_array = variation.to_numpy()
    if layer == None:
        a_data.obsm["X_pc"] = pc_array
        a_data.uns["X_variation"] = variation_array
    else: 
        a_data.obsm[layer + "_variation"] = pc_array
        a_data.uns[layer + "_variation"] = variation_array
    
    os.remove(pc_path)
    os.remove(var_path)

def handle_pc_from_buffer (a_data, layer, pc_str, var_str):

    pc_df = pd.read_csv(StringIO(pc_str), index_col=0)
    var_df = pd.read_csv(StringIO(var_str), index_col=0)
    pc_array = pc_df.to_numpy()
    var_array = var_df.to_numpy()
    if layer is None:
        a_data.obsm["X_pc"] = pc_array
        a_data.uns["X_variation"] = var_array
    else:
        a_data.obsm[layer + "_pc"] = pc_array
        a_data.uns[layer + "_variation"] = var_array

def cidr(a_data, layer=None, data_type = "raw", n_cluster=None, pc=False):
    # Run CIDR-clustering with the R-script
    print("Algorithm Starting...")
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)

    # Creates randomly named temporary files. These are later deleted for the user.
    pc_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    var_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    temp_data_file = tempfile.NamedTemporaryFile(suffix= ".csv", delete = False)
    
    data_path = temp_data_file.name
    pc_path = pc_file.name
    var_path = var_file.name

    pc_file.close()
    var_file.close()
    temp_data_file.close() # garbage collection

    sparse_to_csv(sparse_matrix, data_path)

    (subprocess.run(make_args(data_type, n_cluster, pc, True, data_path, pc_path, var_path), check=True).stderr)

    os.remove(data_path) # cleans up the temp data file.

    print("Algorithm done. Plots are in cidr_plots.pdf")

    if pc == True:
        handle_pc(a_data, layer, pc_path, var_path)

def cidr_non_csv(a_data, layer=None, data_type = "raw", n_cluster=None, pc=False):
    # Run CIDR-clustering with the R-script
    print("Algorithm Starting...")
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    input_data = sparse_to_csv_using_buffer(sparse_matrix)
    result = subprocess.run(
        make_args(data_type, n_cluster, pc, False),
        input=input_data.encode("utf-8"),
        check=True, 
        stdout = subprocess.PIPE
    )

    if pc:
        output = result.stdout.decode("utf-8")

        pc_str, var_str = output.split("---END OF PC---\n")

        handle_pc_from_buffer(a_data, layer, pc_str, var_str)

    print("Algorithm done. Plots are in cidr_plots.pdf")



