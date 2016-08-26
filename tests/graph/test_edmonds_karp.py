from .context import Directed, Undirected, edmonds_karp
from unittest import TestCase

# Figure 6.13 from The Algorithm Design Manual
CASES = [
    {
        'class': Undirected,
        'edges': [
            [0, 1, 5],
            [0, 4, 12],
            [1, 2, 7],
            [1, 3, 9],
            [2, 3, 3],
            [2, 6, 5],
            [3, 5, 3],
            [3, 4, 4],
            [4, 5, 7],
            [5, 6, 2]
        ],
        'from': 0,
        'to': 6,
        'expected': 7
    },
    {
        'class': Undirected,
        'edges': [
            [0, 1, 5],
            [0, 4, 12],
            [1, 2, 7],
            [1, 3, 9],
            [2, 3, 3],
            [2, 6, 5],
            [3, 5, 3],
            [3, 4, 4],
            [4, 5, 7],
            [5, 6, 2]
        ],
        'from': 6,
        'to': 0,
        'expected': 7
    },
    {
        'class': Directed,
        'edges': [
            [0, 1, 5],
            [0, 4, 12],
            [1, 2, 7],
            [1, 3, 9],
            [2, 3, 3],
            [2, 6, 5],
            [3, 5, 3],
            [3, 4, 4],
            [4, 5, 7],
            [5, 6, 2]
        ],
        'from': 0,
        'to': 6,
        'expected': 7
    },
    {
        'class': Directed,
        'edges': [
            [0, 1, 5],
            [0, 4, 12],
            [1, 2, 7],
            [1, 3, 9],
            [2, 3, 3],
            [2, 6, 5],
            [3, 5, 3],
            [3, 4, 4],
            [4, 5, 7],
            [5, 6, 2]
        ],
        'from': 6,
        'to': 0,
        'expected': 0
    }
]


class TestEdmondsKarp(TestCase):
    def test_edmonds_karp(self):
        for case in CASES:
            graph = case['class']()
            for x, y, c in case['edges']:
                graph.insert_edge(x, y, capacity=c)
            result_graph, flow = edmonds_karp(graph, case['from'], case['to'])
            self.assertEqual(case['expected'], flow)
