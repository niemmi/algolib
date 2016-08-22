from unittest import TestCase
from .context import Undirected, Directed, dijkstra, dijkstra_path

CASES = [
    {
        'class': Undirected,
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
        'from': 0,
        'to': 6,
        'expected': [0, 3, 5, 6]
    },
    {
        'class': Undirected,
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
        'from': 1,
        'to': 6,
        'expected': [1, 4, 5, 6]
    },
    {
        'class': Directed,
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
            [6, 5, 2]
        ],
        'from': 0,
        'to': 6,
        'expected': [0, 3, 4, 6]
    }
]


class TestDijkstra(TestCase):
    def test_dijkstra_finds_shortest_path(self):
        for case in CASES:
            graph = case['class']()
            for x, y, w in case['edges']:
                graph.insert_edge(x, y, weight=w)

            result = dijkstra(graph, case['from'], case['to'])
            path = dijkstra_path(result, case['from'], case['to'])
            self.assertEqual(case['expected'], path)

    def test_dijkstra_stops_at_target_vertex(self):
        #     1
        #   /   \
        # 0       3-4
        #   \   /
        #     2
        graph = Undirected()
        graph.insert_edge(0, 1, weight=1)
        graph.insert_edge(0, 2, weight=1)
        graph.insert_edge(1, 3, weight=1)
        graph.insert_edge(2, 3, weight=1)
        graph.insert_edge(3, 4, weight=1)

        for dest in xrange(3):
            result = dijkstra(graph, 0, dest)
            self.assertIsNone(result[4][1])

    def test_dijkstra_unconnected(self):
        #     1
        #   /   \
        # 0       3 4
        #   \   /
        #     2
        graph = Undirected()
        graph.insert_edge(0, 1, weight=1)
        graph.insert_edge(0, 2, weight=1)
        graph.insert_edge(1, 3, weight=1)
        graph.insert_edge(2, 3, weight=1)
        graph.insert_vertex(4)

        for source in xrange(4):
            result = dijkstra(graph, source, 4)
            self.assertIsNone(dijkstra_path(result, source, 4))
