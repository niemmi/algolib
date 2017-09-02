from unittest import TestCase
from .context import Directed, top_sort

EDGES = [
    ['A', 'B'],
    ['A', 'C'],
    ['B', 'C'],
    ['B', 'D'],
    ['C', 'E'],
    ['C', 'F'],
    ['E', 'D'],
    ['F', 'E'],
    ['G', 'A'],
    ['G', 'F'],
]

CASES = [
    [[], ['G', 'A', 'B', 'C', 'F', 'E', 'D']],
    [[['C', 'D']], ['G', 'A', 'B', 'C', 'F', 'E', 'D']],
    [[['E', 'B']], None]
]


class TestTopSort(TestCase):
    def test_top_sort(self):
        graph = Directed()
        for x, y in EDGES:
            graph.insert_edge(x, y)

        for case, expected in CASES:
            copy = graph.copy()
            for x, y in case:
                copy.insert_edge(x, y)
            self.assertEqual(expected, top_sort(copy))
