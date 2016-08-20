from unittest import TestCase
from context import Directed, strong_components

CASES = [
    {
        'class': Directed,
        'edges': [
            [1, 2],
            [2, 3],
            [2, 4],
            [2, 5],
            [3, 1],
            [4, 1],
            [4, 6],
            [4, 8],
            [5, 6],
            [6, 7],
            [7, 5],
            [8, 6]
        ],
        'expected': {
            (1, 2, 3, 4),
            (5, 6, 7),
            (8,)
        }
    }
]

class TestStrongComponents(TestCase):
    def test_strong_components(self):
        for case in CASES:
            graph = case['class']()
            for edge in case['edges']:
                graph.insert_edge(*edge)
            res = {tuple(sorted(c)) for c in strong_components(graph)}
            self.assertEqual(case['expected'], res)
