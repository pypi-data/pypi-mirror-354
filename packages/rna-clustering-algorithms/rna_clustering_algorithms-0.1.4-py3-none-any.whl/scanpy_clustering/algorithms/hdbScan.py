import numpy as np
import hdbscan
from scanpy_clustering.algorithms import register_algorithm
from scanpy_clustering.algorithms.base import BaseAlgorithm

class HDBSCAN(BaseAlgorithm):
    def cluster(self, adata, key_added = 'cluster', **kwargs):
        """
        Applies DBScan clustering to an AnnData object.

        Parameters:
        - adata: AnnData object
        - eps: Set automaticly in HDBSCAN
        - min_samples: The number of samples required to form a dense region.

        Returns:
        - The modified AnnData object with cluster labels stored in adata.obs['dbscan_labels']
        """

        # Extract feature matrix
        X = adata.X
        if isinstance(X, np.ndarray):
            data = X.astype(np.float64)
        else:
            data = X.toarray().astype(np.float64)  # Convert sparse matrix to dense

        # Apply DBScan
        clustering = hdbscan.HDBSCAN(min_cluster_size=kwargs.get("min_cluster_size"), min_samples=kwargs.get("min_samples"))

        # Store results
        adata.obs["dbscan_labels"] = clustering.fit_predict(data) # Convert to string to avoid categorical issues
        return super().cluster(adata, key_added, **kwargs)