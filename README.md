# Spectral Clustering for Nonlinear Structure

Compare Euclidean k-means with graph-based clustering on two moons and concentric rings.

**Author:** Heyang Ma · Independent UCLA graduate course project, revised for this portfolio.
**Tools:** Python / SciPy, Graph Laplacians, Clustering diagnostics. **Scope:** Two synthetic benchmark datasets.

## Question and result

When does a graph representation recover nonlinear cluster geometry that k-means misses?

At the prespecified 10-neighbor setting, normalized spectral clustering achieved ARI 1.0 on both supplied datasets, compared with 0.253 and 0.004 for k-means. The neighbor grid is reported in full, including disconnected-graph diagnostics. These are descriptive benchmark scores, not held-out performance.

![Main result](results/clustering-comparison.png)

## What the analysis does

The executable analysis is [analysis.py](analysis.py). [Methods and interpretation](REPORT.md) explains the scope; [revision notes](REVISION_NOTES.md) distinguish the original analysis from the portfolio revision.

## Run locally

Install Python dependencies with `python -m pip install -r requirements.txt`.
Read [data access and input requirements](DATA_ACCESS.md), then run from this repository:

```sh
python analysis.py --halfmoon data/halfmoon.csv --bullseye data/bullseye.csv --output results
```

## Results and limits

The number of clusters is known for these teaching examples. ARI uses the provided reference labels for evaluation. Affinity choices matter, and perfect recovery of these examples is not evidence of broad generalization. Dense eigendecomposition is not designed for large datasets.

The committed `results/` files are generated summaries from the portfolio revision. Source records, credentials, fitted models, and original notebook outputs are excluded.

## Checks

Run `python -m unittest test_analysis.py`. These tests cover the corrected failure cases; they do not replace statistical validation.
