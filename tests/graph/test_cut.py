from unittest import TestCase
from .context import Undirected, cut_edges, cut_vertices

CASES = [
    {
        'edges': [
            ['a', 'b'],
            ['a', 'c'],
            ['b', 'c'],
            ['c', 'd'],
            ['c', 'f'],
            ['d', 'e'],
            ['e', 'f']
        ],
        'expected_edges': set(),
        'expected_vertices': {'c'}
    },
    {
        'edges': [
            ['a', 'b'],
            ['a', 'c'],
            ['b', 'c'],
            ['c', 'd'],
            ['d', 'e'],
            ['d', 'f'],
            ['e', 'f']
        ],
        'expected_edges': {
            ('c', 'd')
        },
        'expected_vertices': {'c', 'd'}
    },
    {
        'edges': [
            ['a', 'b'],
            ['b', 'c'],
            ['c', 'd'],
            ['c', 'e'],
            ['e', 'f'],
            ['e', 'g'],
            ['e', 'i'],
            ['f', 'g'],
            ['h', 'i']
        ],
        'expected_edges': {
            ('a', 'b'),
            ('b', 'c'),
            ('c', 'd'),
            ('c', 'e'),
            ('e', 'i'),
            ('h', 'i')
        },
        'expected_vertices': {'b', 'c', 'e', 'i'}
    }
]


class TestCut(TestCase):
    @staticmethod
    def create_graph(case):
        graph = Undirected()
        for x, y in case['edges']:
            graph.insert_edge(x, y)

        return graph

    def test_cut_edges(self):
        for case in CASES:
            graph = self.create_graph(case)
            self.assertEqual(case['expected_edges'],
                             {tuple(sorted(edge)) for edge in cut_edges(graph)})

    def test_cut_vertices(self):
        for case in CASES:
            graph = self.create_graph(case)
            self.assertEqual(case['expected_vertices'], cut_vertices(graph))
