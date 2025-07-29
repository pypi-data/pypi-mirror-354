# rnadtu

A Python package for running the CIDR algorithm (originally in R) for clustering single-cell RNA-seq data.

## Features
- Can run the CIDR-Algorithm in Python with the "cidr" function on an AnnData-object with either subprocesses or rpy2.
- cidr function has optional parameters tagType and nClusters, where tagType can be "raw" or "cpm" (counts per million) defaults to "raw". nClusters parameters defaults to algorithms calculation of best amount of clusters, but can be any positive integer. Also added the ability to choose which layer of AnnData is to be clustered.

- cidr_rpy2 function does the same as cidr function but using rpy2 package instead of subprocesses

## Installation
```bash
pip install rnadtu
