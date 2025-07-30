import numpy as np
from sklearn.cluster import KMeans as km
from scanpy_clustering.algorithms import register_algorithm
from scanpy_clustering.algorithms.base import BaseAlgorithm

class KMeans(BaseAlgorithm):
    def cluster(self, 
                adata, 
                key_added = 'cluster', 
                **kwargs) -> None:
        """
        Applies DBScan clustering to an AnnData object.

        Parameters:
        - adata: AnnData object
        - eps: The maximum distance between two samples for them to be considered as in the same neighborhood.
        - min_samples: The number of samples required to form a dense region.
        - metric: The distance metric to use (default: 'euclidean').

        Returns:
        - The modified AnnData object with cluster labels stored in `adata.obs['dbscan_labels']`
        """
        n_clusters = kwargs.get("n_clusters", 8)
        n_init = kwargs.get("n_init", 'auto')
        max_iter = kwargs.get("max_iter", 300)
        # Extract feature matrix
        X = adata.X
        if isinstance(X, np.ndarray):
            data = X
        else:
            data = X.toarray()  # Convert sparse matrix to dense

        # Apply KMeans
        clustering = km(n_clusters=n_clusters, n_init=n_init, max_iter=max_iter).fit(data)
        # Store results
        adata.obs[key_added] = clustering.labels_.astype(str)  # Convert to string to avoid categorical issues
        return #super().cluster(adata, key_added, **kwargs)