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


def make_args(data_type, n_cluster, pc, dropout, dissim, large, file_path=None, pc_path=None, var_path=None, eigen_path=None, dropout_path=None, dissim_path=None):
    # Make an argumentlist to the Rscript."
    script_path = os.path.join(os.path.dirname(__file__), "module2.R")

    return ["Rscript",
            script_path,
            str(data_type),
            str(n_cluster),
            str(pc),
            str(dropout),
            str(dissim),
            str(large),
            str(file_path),
            str(pc_path),
            str(var_path),
            str(eigen_path),
            str(dropout_path),
            str(dissim_path)]


def handle_pc(a_data, layer, pc_path, var_path, eigen_path):
    pc = pd.read_csv(pc_path, index_col=0)
    pc_array = pc.to_numpy()
    variation = pd.read_csv(var_path, index_col=0)
    variation_array = variation.to_numpy()
    eigen = pd.read_csv(var_path, index_col=0)
    eigen_array = eigen.to_numpy()

    if layer == None:
        a_data.obsm["X_cidr_pc"] = pc_array
        a_data.uns["X_cidr_variation"] = variation_array
        a_data.uns["X_cidr_eigenvalues"] = eigen_array
    else:
        a_data.obsm[layer + "_cidr_pc"] = pc_array
        a_data.uns[layer + "_cidr_variation"] = variation_array
        a_data.uns[layer + "_cidr_eigenvalues"] = eigen_array

    os.remove(pc_path)
    os.remove(var_path)
    os.remove(eigen_path)


def handle_dropout(a_data, layer, dropout_path):
    dropout_df = pd.read_csv(dropout_path, index_col=0)
    dropout_array = dropout_df.to_numpy()
    if layer == None:
        a_data.uns["X_cidr_dropout_candidates"] = dropout_array
    else:
        a_data.uns[layer + "_cidr_dropout_candidates"] = dropout_array

    os.remove(dropout_path)


def handle_dissim(a_data, layer, dissim_path):
    dissim_df = pd.read_csv(dissim_path, index_col=0)
    dissim_array = dissim_df.to_numpy()
    if layer == None:
        a_data.obsp["X_cidr_dissimilarity_matrix"] = dissim_array
    else:
        a_data.obsp[layer + "_cidr_dissimilarity_matrix"] = dissim_array

    os.remove(dissim_path)


def handle_pc_from_buffer(a_data, layer, pc_str, var_str, egien_str):
    pc_df = pd.read_csv(StringIO(pc_str), index_col=0)
    var_df = pd.read_csv(StringIO(var_str), index_col=0)
    eigen_df = pd.read_csv(StringIO(egien_str), index_col=0)

    pc_array = pc_df.to_numpy()
    var_array = var_df.to_numpy()
    eigen_array = eigen_df.to_numpy()

    if layer is None:
        a_data.obsm["X_cidr_pc"] = pc_array
        a_data.uns["X_cidr_variation"] = var_array
        a_data.uns["X_cidr_eigenvalues"] = eigen_array
    else:
        a_data.obsm[layer + "_cidr_pc"] = pc_array
        a_data.uns[layer + "_cidr_variation"] = var_array
        a_data.uns[layer + "_cidr_eigenvalues"] = eigen_array



def handle_dropout_from_buffer(a_data, layer, dropout_str):
    dropout_df = pd.read_csv(StringIO(dropout_str), index_col=0)
    dropout_array = dropout_df.to_numpy()
    if layer is None:
        a_data.uns["X_cidr_dropout_candidates"] = dropout_array
    else:
        a_data.uns[layer + "_cidr_dropout_candidates"] = dropout_array


def handle_dissim_from_buffer(a_data, layer, dissim_str):
    dissim_df = pd.read_csv(StringIO(dissim_str), index_col=0)
    dissim_array = dissim_df.to_numpy()
    if layer is None:
        a_data.obsp["X_cidr_dissimilarity_matrix"] = dissim_array
    else:
        a_data.obsp[layer + "_cidr_dissimilarity_matrix"] = dissim_array


def cidr(a_data, layer=None, data_type="raw", n_cluster=None, dropout=False, dissim=False, pc=False):
    # Run CIDR-clustering
    print("Algorithm Starting...")
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)

    # Creates randomly named temporary files. These are later deleted for the user.
    pc_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    var_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    eigen_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    temp_data_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    dropout_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    dissim_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)

    # Sets path for different datafiles for use to read and write in R-script.
    data_path = temp_data_file.name
    pc_path = pc_file.name
    var_path = var_file.name
    eigen_path = eigen_file.name
    dropout_path = dropout_file.name
    dissim_path = dissim_file.name

    # Closes the files to save ram
    pc_file.close()
    var_file.close()
    eigen_file.close()
    temp_data_file.close()
    dropout_file.close()
    dissim_file.close() # garbage collection

    # Saves sparse matrix as csv and then runs the Rscript on the file.
    sparse_to_csv(sparse_matrix, data_path)
    (subprocess.run(make_args(data_type, n_cluster, pc, dropout, dissim,
                              True, data_path, pc_path, var_path,
                              eigen_path, dropout_path, dissim_path), check=True).stderr)

    # Cleans up the temp data file.
    os.remove(data_path)

    if dropout:
        handle_dropout(a_data, layer, dropout_path)

    if dissim:
        handle_dissim(a_data, layer, dissim_path)

    # If pc true in cidr function, then principal coordinates is put in a_data object.
    if pc:
        handle_pc(a_data, layer, pc_path, var_path, eigen_path)

    print("Algorithm done. Plots are in cidr_plots.pdf")


def cidr_non_csv(a_data, layer=None, data_type="raw", n_cluster=None, dropout=False, dissim=False, pc=False):
    # Run CIDR-clustering
    print("Algorithm Starting...")
    data = a_data.X if layer is None else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    input_data = sparse_to_csv_using_buffer(sparse_matrix)
    # Runs the R-Script on the input_data
    result = subprocess.run(
        make_args(data_type, n_cluster, pc, dropout, dissim, False),
        input=input_data.encode("utf-8"),
        check=True,
        stdout=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8")

    if dropout:
        dropout_str, output = output.split("---END OF DROPOUT CANDIDATES---\n")
        handle_dropout_from_buffer(a_data, layer, dropout_str)

    if dissim:
        dissim_str, output = output.split("---END OF DISSIMILARITY---\n")
        handle_dissim_from_buffer(a_data, layer, dissim_str)

    # If pc true in cidr function, then principal coordinates it put in a_data object.
    if pc:
        pc_str, var_str = output.split("---END OF PC---\n")
        egien_str, output = var_str.split("---END OF VARIATION---\n")
        handle_pc_from_buffer(a_data, layer, pc_str, var_str, egien_str)


    print("Algorithm done. Plots are in cidr_plots.pdf")
