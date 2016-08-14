import unittest
from .context import Undirected, Directed, BFS
from collections import deque, OrderedDict
from itertools import groupby

EDGES = [
    [8, 4],
    [4, 1],
    [1, 0],
    [1, 3],
    [1, 5],
    [0, 2],
    [3, 5],
    [2, 6],
    [2, 7]
]

ORDER = [8, 4, 1, 0, 3, 5, 2, 6, 7]

class TestBFSUndirected(unittest.TestCase):
    def setUp(self):
        self.g = Undirected()

        for x, y in EDGES:
            self.g.insert_edge(x, y)

        # Hackery to ensure the order children are processed
        for v, d in self.g._neighbors.iteritems():
            self.g._neighbors[v] = OrderedDict(sorted(d.iteritems()))

    def test_call_process_vertex_early(self):
        bfs = None
        order = deque(ORDER)

        def hook(graph, cb_bfs, vertex_name):
            self.assertIs(self.g, graph)
            self.assertIs(bfs, cb_bfs)
            self.assertEqual(order.popleft(), vertex_name)
            vertex = cb_bfs[vertex_name]
            parent = next((x[0] for x in EDGES if x[1] == vertex_name), None)
            self.assertEqual(parent, vertex.parent)
            self.assertEqual(BFS.DISCOVERED, vertex.state)

        bfs = BFS(self.g, process_vertex_early=hook)
        bfs.execute(8)
        self.assertFalse(order)

    def test_call_process_vertex_late(self):
        bfs = None
        order = deque(ORDER)
        early_called = set()

        def early_hook(_graph, _cb_bfs, vertex_name):
            early_called.add(vertex_name)

        def hook(graph, cb_bfs, vertex_name):
            self.assertIs(self.g, graph)
            self.assertIs(bfs, cb_bfs)
            self.assertEqual(order.popleft(), vertex_name)
            vertex = cb_bfs[vertex_name]
            self.assertIn(vertex_name, early_called)
            self.assertEqual(BFS.PROCESSED, vertex.state)

        bfs = BFS(self.g, process_vertex_early=early_hook,
                  process_vertex_late=hook)
        bfs.execute(8)
        self.assertFalse(order)

    def test_call_process_edge(self):
        bfs = None
        order = deque(EDGES)

        def hook(graph, cb_bfs, source, dest, edge):
            self.assertIs(self.g, graph)
            self.assertIs(bfs, cb_bfs)
            self.assertEqual(tuple(sorted(order.popleft())), edge)
            self.assertEqual(tuple(sorted([source, dest])), edge)
            self.assertEqual(BFS.PROCESSED, cb_bfs[source].state)

        bfs = BFS(self.g, process_edge=hook)
        bfs.execute(8)
        self.assertFalse(order)
