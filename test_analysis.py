"""Known disconnected blocks should be recovered without reference-label fitting."""

import unittest
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from analysis import spectral_embedding


class GraphChecks(unittest.TestCase):
    def test_three_blocks_need_three_eigenvectors(self):
        graph = np.kron(np.eye(3), np.ones((4, 4)) - np.eye(4))
        embedding, components = spectral_embedding(graph, 3)
        prediction = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(
            embedding
        )
        self.assertEqual(components, 3)
        self.assertEqual(adjusted_rand_score(np.repeat(range(3), 4), prediction), 1.0)

    def test_isolated_node_is_rejected(self):
        graph = np.ones((5, 5)) - np.eye(5)
        graph[0, :] = 0
        graph[:, 0] = 0
        with self.assertRaises(ValueError):
            spectral_embedding(graph, 2)


if __name__ == "__main__":
    unittest.main()
