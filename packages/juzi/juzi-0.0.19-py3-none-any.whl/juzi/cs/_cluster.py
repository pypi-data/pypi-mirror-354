import warnings
import numpy as np
import scipy as sp

from anndata import AnnData
from typing import Tuple
from scipy.cluster.hierarchy import ClusterWarning
from sklearn.metrics import silhouette_score


def cluster(
    adata: AnnData,
    threshold: float = 0.1,
    min_cluster: int = 1,
    silent: bool = False,
    copy: bool = False
) -> AnnData | None:
    """Cluster the factor similarity matrix by iterative merging.

    Parameters
    ----------
    adata : AnnData
        AnnData object fit with juzi.cs.nmf.
    threshold : float
        Merge elements/clusters until the maximum similarity between clusters
        reduces to the specified similarity threshold. A value closer to 1 will
        create more clusters. A value closer to 0 will create fewer clusters.
    min_cluster : int
        Minimum number of unique labels/samples contributing. Note that the 
        labels/samples were given in the .nmf key argument.
    silent : bool
        If True, disable progress bar.
    copy : bool
        If True, a copy of the anndata is returned.
    """
    if "juzi_similarity" not in adata.uns or "juzi_names" not in adata.uns:
        raise KeyError("Please run juzi.cs.similarity before clustering.")

    if threshold < 0. or threshold > 1.:
        raise ValueError("'threshold' must be in [0, 1]")

    mask = np.ones(adata.uns["juzi_similarity"].shape[0], dtype=bool)
    if "juzi_keep" in adata.uns:
        mask = np.array(adata.uns["juzi_keep"], dtype=bool)

    drop_min_cluster = True
    while drop_min_cluster:
        S = adata.uns["juzi_similarity"][:, mask][mask, :]
        labels = np.array(adata.uns["juzi_names"])[mask]

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ClusterWarning)
            Z = sp.cluster.hierarchy.linkage(
                1.-S, method="average", optimal_ordering=True)

        leaf_order = sp.cluster.hierarchy.leaves_list(Z)
        clusters = np.empty(S.shape[0], dtype=int)
        for new_label, idx in enumerate(leaf_order):
            clusters[idx] = new_label

        while True:
            max_pair = _find_max_similar(S, clusters, threshold)
            if max_pair is None:
                break

            i, j = max_pair
            clusters[clusters == clusters[j]] = clusters[i]

        counts = []
        assignments = np.unique(clusters)
        for c in assignments:
            c_mask = np.array(clusters == c, dtype=bool)
            c_name = labels[c_mask]
            counts.append(len(np.unique(c_name)))

        counts = np.array(counts)
        if np.sum(counts < min_cluster) == 0:
            adata.uns["juzi_keep"] = mask
            break

        mask = np.isin(clusters, assignments[counts >= min_cluster])

        if np.sum(mask) == 0:
            raise ValueError(
                "No elements remain after removal. Try lowering 'min_cluster'.")

    adata.uns["juzi_cluster_stats"] = {
        "silhouette_score": None,
        "outer_similarity": np.mean(S[clusters[:, None] != clusters[None, :]]),
        "inner_similarity": np.mean(S[clusters[:, None] == clusters[None, :]]),
    }

    nc = len(np.unique(clusters))
    if nc > 1 and nc < S.shape[0] - 1:
        adata.uns["juzi_cluster_stats"]["silhouette_score"] = silhouette_score(
            S, clusters)

    adata.uns["juzi_cluster_labels"] = labels
    adata.uns["juzi_cluster_groups"] = clusters
    adata.uns["juzi_cluster_linkage"] = Z

    return adata if copy else None


def _find_max_similar(
    S: np.ndarray,
    clusters: np.ndarray,
    threshold: float,
) -> Tuple[int, int] | None:
    # Unique labels and the first index for each group
    c_unique, first_indices = np.unique(clusters, return_index=True)
    c_counts = np.array([np.sum(clusters == ul) for ul in c_unique])

    # We can use an indicator matrix (N x U) to track indices
    X = (clusters[:, None] == c_unique[None, :]).astype(float)

    # Compute sum of similarities for each pair of clusters (generates a U x U)
    # matrix where each entry (i, j) specifies sum between rows (i, j) in S.
    sum_sims = X.T @ S @ X

    # Dividing by outer product of label counts gives mean similarity of (i, j)
    mean_sims = sum_sims / np.outer(c_counts, c_counts)

    # Mask the diagonal to ensure we don't group the same entries
    np.fill_diagonal(mean_sims, -np.inf)

    best_idx = np.argmax(mean_sims)
    max_similarity = mean_sims.flat[best_idx]

    if max_similarity > threshold:
        group_i, group_j = np.unravel_index(best_idx, mean_sims.shape)
        best_pair = (first_indices[group_i], first_indices[group_j])
    else:
        best_pair = None

    if best_pair is None:
        return None

    i, j = best_pair

    return i, j
