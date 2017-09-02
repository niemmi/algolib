from unittest import TestCase
from .context import Undirected, Directed, DFS
from collections import OrderedDict

EDGES = [
    [8, 4],
    [4, 1],
    [1, 0],
    [1, 3],
    [1, 5],
    [0, 2],
    [2, 6],
    [2, 7],
    [3, 5]
]

PARENT = {
    8: [],
    4: [8],
    1: [4],
    0: [1],
    3: [1, 5],
    5: [1, 3],
    2: [0],
    6: [2],
    7: [2]
}

CATEGORIES = {
    (8, 4): DFS.TREE,
    (4, 1): DFS.TREE,
    (1, 0): DFS.TREE,
    (1, 3): DFS.TREE,
    (1, 5): DFS.TREE,
    (3, 1): DFS.BACK,
    (5, 1): DFS.BACK,
    (5, 3): DFS.TREE,
    (3, 5): DFS.TREE,
    (0, 2): DFS.TREE,
    (2, 6): DFS.TREE,
    (2, 7): DFS.TREE
}


class TestDFSUndirected(TestCase):
    def setUp(self):
        self.g = Undirected()
        for x, y in EDGES:
            self.g.insert_edge(x, y)

    def test_call_process_vertex_early(self):
        dfs = None
        called = set()

        def hook(graph, cb_dfs, vertex_name):
            self.assertIs(self.g, graph)
            self.assertIs(dfs, cb_dfs)
            vertex = cb_dfs[vertex_name]
            if PARENT[vertex_name]:
                self.assertTrue(any(x in called for x in PARENT[vertex_name]))
                self.assertIn(vertex.parent, PARENT[vertex_name])
                self.assertEqual(vertex.state, DFS.DISCOVERED)
                self.assertGreater(vertex.entry, cb_dfs[vertex.parent].entry)
            called.add(vertex_name)

        dfs = DFS(self.g, process_vertex_early=hook)
        dfs.execute(8)
        self.assertEqual(set(self.g.vertices.keys()), called)

    def test_call_process_edge(self):
        dfs = None
        edges = {tuple(sorted(edge)) for edge in EDGES}

        def hook(graph, cb_dfs, source, dest, edge):
            self.assertIs(self.g, graph)
            self.assertIs(dfs, cb_dfs)
            self.assertEqual(edge, tuple(sorted([source, dest])))
            edges.remove(edge)

            if dfs[dest].state == DFS.UNDISCOVERED:
                self.assertIn(source, PARENT[dest])

            return True

        dfs = DFS(self.g, process_edge=hook)
        dfs.execute(8)
        self.assertFalse(edges)

    def test_process_edge_result(self):
        count = [0]

        def edge_hook(*_):
            return False

        def vertex_hook(*_):
            count[0] += 1

        bfs = DFS(self.g, process_vertex_early=vertex_hook,
                  process_edge=edge_hook)
        bfs.execute(8)
        self.assertEqual(1, count[0])

    def test_call_process_vertex_late(self):
        dfs = None
        called = set()

        def hook(graph, cb_dfs, vertex):
            self.assertIs(self.g, graph)
            self.assertIs(dfs, cb_dfs)
            self.assertTrue(all(cb_dfs[x].state == DFS.PROCESSED
                                for x in self.g.vertices
                                if cb_dfs[x].parent == vertex))
            called.add(vertex)

        dfs = DFS(self.g, process_vertex_late=hook)
        dfs.execute(8)
        self.assertEqual(set(self.g.vertices.keys()), called)

    def test_edge_category(self):
        def hook(_graph, dfs, source, dest, _edge):
            category = dfs.edge_category(source, dest)
            self.assertEqual(CATEGORIES[(source, dest)], category)

        DFS(self.g, process_edge=hook).execute(8)

PARENT_DIRECTED = {
    0: None,
    1: 0,
    2: 0,
    3: 1,
    4: 1
}

CATEGORIES_DIRECTED = {
    (0, 1): DFS.TREE,
    (0, 2): DFS.TREE,
    (0, 4): DFS.FORWARD,
    (1, 3): DFS.TREE,
    (1, 4): DFS.TREE,
    (2, 1): DFS.CROSS,
    (3, 0): DFS.BACK
}


class TestDFSDirected(TestCase):
    def setUp(self):
        self.g = Directed()
        for x, y in CATEGORIES_DIRECTED:
            self.g.insert_edge(x, y)

        # Hackery to ensure the order children are processed
        for v, d in self.g._outgoing.items():
            self.g._outgoing[v] = OrderedDict(sorted(d.items()))

    def test_edge_category(self):
        def hook(_, dfs, x, y, e):
            self.assertEqual(CATEGORIES_DIRECTED[e], dfs.edge_category(x, y))
            return True

        DFS(self.g, process_edge=hook).execute(0)
