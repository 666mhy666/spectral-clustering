"""Graph clustering with separate neighborhood size and cluster count."""

from pathlib import Path
import argparse, json, warnings
import numpy as np
import pandas as pd
from scipy.linalg import eigh
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import KMeans
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics import adjusted_rand_score, pairwise_distances
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def spectral_embedding(affinity, k):
    a = np.asarray(affinity, dtype=float)
    if (
        a.ndim != 2
        or a.shape[0] != a.shape[1]
        or not np.allclose(a, a.T)
        or np.any(a < 0)
    ):
        raise ValueError("Affinity must be square, symmetric and nonnegative")
    if not 1 < k < a.shape[0]:
        raise ValueError("Invalid cluster count")
    degree = a.sum(axis=1)
    if np.any(degree <= 0):
        raise ValueError("Isolated node; change graph parameters")
    components = connected_components(
        csr_matrix(a), directed=False, return_labels=False
    )
    if components > k:
        warnings.warn(
            f"Graph has {components} components for {k} requested clusters",
            RuntimeWarning,
        )
    normalized = a / np.sqrt(degree[:, None] * degree[None, :])
    _, vectors = eigh(normalized, subset_by_index=(a.shape[0] - k, a.shape[0] - 1))
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.maximum(norms, np.finfo(float).eps), components


def spectral_knn(X, neighbors, k, seed=42):
    if not 1 <= neighbors < len(X):
        raise ValueError("Invalid neighbor count")
    a = kneighbors_graph(
        X, neighbors, mode="connectivity", include_self=False
    ).toarray()
    z, c = spectral_embedding(np.maximum(a, a.T), k)
    return KMeans(n_clusters=k, n_init=20, random_state=seed).fit_predict(z), c


def spectral_rbf(X, sigma2, k, seed=42):
    if sigma2 <= 0:
        raise ValueError("sigma2 must be positive")
    a = np.exp(-pairwise_distances(X, squared=True) / (2 * sigma2))
    np.fill_diagonal(a, 0)
    z, c = spectral_embedding(a, k)
    return KMeans(n_clusters=k, n_init=20, random_state=seed).fit_predict(z), c


def run(halfmoon, bullseye, out):
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    fig, axes = plt.subplots(2, 3, figsize=(10, 6.5), layout="constrained")
    for row, (name, file, k, sigma2) in enumerate(
        [("Halfmoon", halfmoon, 2, 0.01), ("Bullseye", bullseye, 3, 0.1)]
    ):
        d = pd.read_csv(file)
        X = d[["X1", "X2"]].to_numpy()
        y = d.Cluster.to_numpy()
        if not np.isfinite(X).all():
            raise ValueError("Non-finite coordinates")
        labels = KMeans(n_clusters=k, n_init=20, random_state=42).fit_predict(X)
        rows.append(
            dict(
                dataset=name,
                method="k-means",
                neighbors=None,
                k=k,
                components=None,
                ari=adjusted_rand_score(y, labels),
            )
        )
        plotted = [("k-means", labels)]
        for m in [5, 10, 15, 20]:
            labels, c = spectral_knn(X, m, k)
            rows.append(
                dict(
                    dataset=name,
                    method="kNN spectral",
                    neighbors=m,
                    k=k,
                    components=c,
                    ari=adjusted_rand_score(y, labels),
                )
            )
            if m == 10:
                plotted.append(("kNN spectral, neighbors=10", labels))
        labels, c = spectral_rbf(X, sigma2, k)
        plotted.append(("RBF spectral", labels))
        rows.append(
            dict(
                dataset=name,
                method="RBF spectral",
                neighbors=None,
                k=k,
                components=c,
                ari=adjusted_rand_score(y, labels),
            )
        )
        for ax, (method, labels) in zip(axes[row], plotted):
            ax.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", s=9)
            ax.set_title(f"{name}: {method}", fontsize=10)
            ax.set_xlabel("X1")
            ax.set_ylabel("X2")
    results = pd.DataFrame(rows)
    results.to_csv(out / "clustering-comparison.csv", index=False)
    fig.savefig(out / "clustering-comparison.png", dpi=170)
    plt.close(fig)
    (out / "run.json").write_text(
        json.dumps(
            {
                "seed": 42,
                "cluster_counts": {"Halfmoon": 2, "Bullseye": 3},
                "interpretation": "Descriptive benchmark with known cluster counts. Labels used only to report ARI; no held-out generalization claim.",
            },
            indent=2,
        )
    )
    print(results.to_string(index=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--halfmoon", type=Path, required=True)
    p.add_argument("--bullseye", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("results"))
    a = p.parse_args()
    run(a.halfmoon, a.bullseye, a.output)
