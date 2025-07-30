import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import scanpy as sc
from src.resolutiontree import cluster_resolution_finder, cluster_decision_tree

# Load the dataset
adata = sc.datasets.pbmc3k()

# Perform standard preprocessing
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

resolutions = [0.0, 0.2, 0.5, 1.0, 1.5, 2.0]

adata_discovery = adata.copy()

# Perform hierarchical clustering with different resolutions
cluster_resolution_finder(adata_discovery,
                          resolutions=resolutions,
                          n_top_genes=3, 
                          min_cells=2,
                          deg_mode="within_parent"
                          )

cluster_decision_tree(adata_discovery, resolutions=resolutions, 
                      output_settings = {
                          "output_path": "tests/expected.png",
                          "draw": False,
                          "figsize": (12, 8),
                          "dpi": 300
                          },
                      node_style = {
                          "node_size": 500,
                          "node_colormap": None,
                          "node_label_fontsize": 12
                          },
                      edge_style = {
                          "edge_color": "parent",
                          "edge_curvature": 0.01,
                          "edge_threshold": 0.01,
                          "show_weight": True,
                          "edge_label_threshold": 0.05,
                          "edge_label_position": 0.8,
                          "edge_label_fontsize": 8
                          },
                      gene_label_settings = {
                          "show_gene_labels": True,
                          "n_top_genes": 2,
                          "gene_label_threshold": 0.001,
                          "gene_label_style": {"offset":0.5, "fontsize":8},
                        },
                      level_label_style = {
                          "level_label_offset": 15,
                          "level_label_fontsize": 12
                        },
                      title_style = {
                          "title": "Hierarchical Leiden Clustering",
                          "title_fontsize": 20
                        },
                      layout_settings = {
                          "node_spacing": 5.0,
                          "level_spacing": 1.5
                        },
                      clustering_settings = {
                          "prefix": "leiden_res_",
                          "edge_threshold": 0.05
                        }
                    )