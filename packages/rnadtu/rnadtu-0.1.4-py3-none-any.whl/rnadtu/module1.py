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


def make_args(data_type, n_cluster, pc, drop_cand, large, file_path=None, pc_path=None, var_path=None, drop_cand_path=None):
    # Make an argumentlist to the Rscript."
    script_path = os.path.join(os.path.dirname(__file__), "module2.R")

    return ["Rscript",
            script_path,
            str(data_type),
            str(n_cluster),
            str(pc),
            str(drop_cand),
            str(large),
            str(file_path),
            str(pc_path),
            str(var_path),
            str(drop_cand_path)]


def handle_pc(a_data, layer, pc_path, var_path):
    pc = pd.read_csv(pc_path, index_col=0)
    pc_array = pc.to_numpy()
    variation = pd.read_csv(var_path, index_col=0)
    variation_array = variation.to_numpy()
    if layer == None:
        a_data.obsm["X_pc"] = pc_array
        a_data.uns["X_variation"] = variation_array
    else:
        a_data.obsm[layer + "_pc"] = pc_array
        a_data.uns[layer + "_variation"] = variation_array

    os.remove(pc_path)
    os.remove(var_path)


def handle_drop_cand(a_data, layer, drop_cand_path):
    drop_cand = pd.read_csv(drop_cand_path, index_col=0)
    drop_cand_array = drop_cand.to_numpy()
    if layer == None:
        a_data.uns["X_dropout_candidates"] = drop_cand_array
    else:
        a_data.uns[layer + "_dropout_candidates"] = drop_cand_array

    os.remove(drop_cand_path)


def handle_pc_from_buffer(a_data, layer, pc_str, var_str):

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


def handle_drop_cand_from_buffer(a_data, layer, drop_cand_str):

    drop_cand_df = pd.read_csv(StringIO(drop_cand_str), index_col=0)
    drop_cand_array = drop_cand_df.to_numpy()
    if layer is None:
        a_data.uns["X_dropout_candidates"] = drop_cand_array
    else:
        a_data.uns[layer + "_dropout_candidates"] = drop_cand_array


def cidr(a_data, layer=None, data_type="raw", n_cluster=None, pc=False, drop_cand=False):
    # Run CIDR-clustering
    print("Algorithm Starting...")
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)

    # Creates randomly named temporary files. These are later deleted for the user.
    pc_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    var_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    temp_data_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    drop_cand_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)

    # Sets path for different datafiles for use to read and write in R-script.
    data_path = temp_data_file.name
    pc_path = pc_file.name
    var_path = var_file.name
    drop_cand_path = drop_cand_file.name

    # Closes the files to save ram
    pc_file.close()
    var_file.close()
    temp_data_file.close()
    drop_cand_file.close() # garbage collection

    # Saves sparse matrix as csv and then runs the Rscript on the file.
    sparse_to_csv(sparse_matrix, data_path)
    (subprocess.run(make_args(data_type, n_cluster, pc, drop_cand,
     True, data_path, pc_path, var_path, drop_cand_path), check=True).stderr)

    # Cleans up the temp data file.
    os.remove(data_path)

    # If pc true in cidr function, then principal coordinates is put in a_data object.
    if pc:
        handle_pc(a_data, layer, pc_path, var_path)

    if drop_cand:
        handle_drop_cand(a_data, layer, drop_cand_path)

    print("Algorithm done. Plots are in cidr_plots.pdf")


def cidr_non_csv(a_data, layer=None, data_type="raw", n_cluster=None, pc=False, drop_cand=False):
    # Run CIDR-clustering
    print("Algorithm Starting...")
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    input_data = sparse_to_csv_using_buffer(sparse_matrix)
    # Runs the R-Script on the input_data
    result = subprocess.run(
        make_args(data_type, n_cluster, pc, drop_cand, False),
        input=input_data.encode("utf-8"),
        check=True,
        stdout=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8")

    if drop_cand:
        drop_cand_str, output = output.split("---END OF DROPOUT CANDIDATES---\n")
        handle_drop_cand_from_buffer(a_data, layer, drop_cand_str)

    # If pc true in cidr function, then principal coordinates it put in a_data object.
    if pc:
        pc_str, var_str = output.split("---END OF PC---\n")
        handle_pc_from_buffer(a_data, layer, pc_str, var_str)


    print("Algorithm done. Plots are in cidr_plots.pdf")
