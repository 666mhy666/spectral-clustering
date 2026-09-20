# Methods and interpretation

## Question

When does a graph representation recover nonlinear cluster geometry that k-means misses?

## Data

Two synthetic benchmark datasets. Exact results use the two supplied teaching CSVs, not redistributed here. Each requires X1, X2, Cluster. The labels are used only to describe recovery, not to fit the clustering models. Other synthetic inputs can be supplied but will produce different scores.

## Analysis

I implemented normalized graph-Laplacian clustering, compared it with k-means, and reported adjusted Rand index, graph connectivity, and isolated-node diagnostics across a neighbor grid.

The entry point is `analysis.py`. Parameters, variables, assumptions, and analysis cohorts are recorded in the code and generated result files.

## Findings

At 10 neighbors, normalized spectral clustering achieved ARI 1.0 on both supplied datasets, compared with 0.253 and 0.004 for k-means. The neighbor grid is reported in full, including disconnected-graph diagnostics. These are descriptive benchmark scores, not held-out performance.

![K-means and normalized spectral-clustering assignments on the two supplied datasets.](results/clustering-comparison.png)

_K-means and normalized spectral-clustering assignments on the two supplied datasets._

## Assumptions and interpretation

The number of clusters is known for these teaching examples. ARI uses the provided reference labels for evaluation. Affinity choices matter, and perfect recovery of these examples is not evidence of broad generalization. Dense eigendecomposition is not designed for large datasets.

## Result files

- [clustering-comparison.csv](results/clustering-comparison.csv)
- [clustering-comparison.png](results/clustering-comparison.png)
- [run.json](results/run.json)
