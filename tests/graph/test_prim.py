from unittest import TestCase
from .context import Undirected, prim

CASES = [
    {
        'edges': [
            [0, 1, 2],
            [0, 2, 3],
            [1, 2, 4]
        ],
        'expected': 5
    },
    {
        'edges': [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 5],
            [1, 2, 1],
            [1, 3, 2],
            [2, 4, 2],
            [3, 4, 3]
        ],
        'expected': 7
    },
    {
        'edges': [
            [0, 1, 5],
            [0, 2, 12],
            [0, 3, 7],
            [1, 3, 9],
            [1, 4, 7],
            [2, 3, 4],
            [2, 5, 7],
            [3, 4, 4],
            [3, 5, 3],
            [4, 5, 2],
            [4, 6, 5],
            [5, 6, 2]
        ],
        'expected': 23
    }
]


class TestPrim(TestCase):
    def test_prim(self):
        for case in CASES:
            graph = Undirected()
            for x, y, weight in case['edges']:
                graph.insert_edge(x, y, weight=weight)

            self.assertEqual(case['expected'],
                             sum(graph[x][y]['weight'] for x, y in prim(graph)))
