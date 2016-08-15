import unittest
from .context import Undirected, BFS, bipartite

EDGES = [
    [8, 4],
    [4, 1],
    [1, 0],
    [1, 3],
    [1, 5],
    [0, 2],
    [2, 2],
    [2, 6],
    [2, 7]
]

CASES = [
    [[], True],
    [[[3, 7]], False],
    [[[3, 5]], False],
    [[[7, 9], [9, 3]], True],
    [[[8, 1]], False]
]


class TestBipartite(unittest.TestCase):
    def test_bipartite(self):
        graph = Undirected()
        for x, y in EDGES:
            graph.insert_edge(x, y)

        for case, expected in CASES:
            copy = graph.copy()
            for x, y in case:
                copy.insert_edge(x, y)
            self.assertEqual(expected, bipartite(copy), str(case) + ' fails')
