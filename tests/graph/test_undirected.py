import unittest
from .context import Undirected
from collections import Counter

EDGES = [
    [8, 4],
    [4, 1],
    [1, 0],
    [1, 3],
    [1, 5],
    [0, 2],
    [2, 2],
    [2, 6],
    [2, 7],
    [7, 3]
]


class TestUndirected(unittest.TestCase):
    @staticmethod
    def initialize_graph():
        graph = Undirected()
        for x, y in EDGES:
            graph.insert_edge(x, y)

        return graph

    def setUp(self):
        self.g = self.initialize_graph()

    def test_insert_vertex_adds_vertex(self):
        self.assertNotIn(9, self.g.vertices)
        self.g.insert_vertex(9)
        self.assertIn(9, self.g.vertices)

    def test_insert_vertex_takes_kwargs(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_vertex(9, **kwargs)
        self.assertEqual(kwargs, self.g.vertices[9])

    def test_insert_vertex_doesnt_override_existing_edges(self):
        neighbors = set(self.g[7].keys())
        degree = self.g.degree(7)
        self.g.insert_vertex(7)
        self.assertEqual(neighbors, self.g[7].keys())
        self.assertEqual(degree, self.g.degree(7))

    def test_insert_vertex_doesnt_override_existing_properties(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_vertex(9, **kwargs)
        kwargs2 = {'bar': 'foo'}
        self.g.insert_vertex(9, **kwargs2)
        kwargs.update(kwargs2)
        self.assertEqual(kwargs, self.g.vertices[9])

    def test_remove_vertex_removes_vertex(self):
        for v in tuple(self.g.vertices.keys()):
            self.g.remove_vertex(v)
            self.assertNotIn(v, self.g.vertices)

    def test_remove_vertex_removes_edges(self):
        self.g.remove_vertex(2)
        self.assertNotIn(2, self.g._neighbors)

        for v in self.g.vertices:
            self.assertNotIn(2, self.g._neighbors[v])

        for e in self.g.edges:
            self.assertNotIn(2, e)

    def test_remove_vertex_removes_properties(self):
        self.g.insert_vertex(8, foo='bar')
        self.g.remove_vertex(8)
        self.g.insert_vertex(8)
        self.assertEqual({}, self.g.vertices[8])

    def test_insert_edge_adds_edge(self):
        self.assertFalse(any(e in self.g.edges for e in [(7, 5), (5, 7)]))

        for x, y in [[7, 5], [5, 7]]:
            self.assertNotIn(x, self.g[y])
            self.assertNotIn(y, self.g[x])
            self.assertFalse(any(e in self.g.edges for e in [(x, y), (y, x)]))
            self.g.insert_edge(x, y)
            self.assertIn(x, self.g[y])
            self.assertIn(y, self.g[x])
            self.assertTrue(any(e in self.g.edges for e in [(x, y), (y, x)]))
            self.g.remove_edge(x, y)

    def test_insert_edge_creates_vertex(self):
        self.g.insert_edge(8, 9)

        self.assertIn(9, self.g[8])
        self.assertIn(8, self.g[9])

    def test_insert_edge_takes_kwargs(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_edge(7, 5, **kwargs)

        self.assertEqual(kwargs, self.g[7][5])
        self.assertEqual(kwargs, self.g[5][7])
        self.assertEqual(kwargs, self.g.edges[tuple(sorted([7, 5]))])

    def test_insert_edge_doesnt_override_existing(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_edge(7, 5, **kwargs)
        self.g.insert_edge(5, 7)

        self.assertEqual(kwargs, self.g[7][5])
        self.assertEqual(kwargs, self.g[5][7])
        self.assertEqual(kwargs, self.g.edges[tuple(sorted([7, 5]))])

    def test_remove_edge_removes_properties(self):
        self.g.insert_edge(2, 6, foo='bar')
        self.g.remove_edge(6, 2)
        self.g.insert_edge(2, 6)

        self.assertEqual({}, self.g[2][6])
        self.assertEqual({}, self.g[6][2])
        self.assertEqual({}, self.g.edges[tuple(sorted([6, 2]))])

    def test_connected(self):
        for x, y in EDGES:
            self.assertTrue(self.g.connected(x, y))
            self.assertTrue(self.g.connected(y, x))

    def test_edges_between(self):
        for x in self.g.vertices:
            for y in self.g.vertices:
                self.assertEqual(self.g.connected(x, y),
                                 len(list(self.g.edges_between(x, y))))
                self.assertEqual(self.g.connected(x, y),
                                 len(list(self.g.edges_between(y, x))))

    def test_edges_from(self):
        edges = set(tuple(e) for e in EDGES)
        for v in self.g.vertices:
            edges.difference_update(e for e, _ in self.g.edges_from(v))

        self.assertEqual(next(self.g.edges_from(8)), ((4, 8), 4))

    def test_degree(self):
        c = Counter(v for e in self.g.edges for v in e)
        for v in self.g.vertices:
            self.assertEqual(c[v], self.g.degree(v))

    def test_eq(self):
        other = self.initialize_graph()
        self.assertEqual(self.g, other)

        other.insert_vertex(9)
        self.assertNotEqual(self.g, other)
        other.remove_vertex(9)

        other.vertices[4]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.vertices[4]['foo']

        other.insert_edge(6, 7)
        self.assertNotEqual(self.g, other)
        other.remove_edge(6, 7)

        other.edges[(4, 8)]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.edges[(4, 8)]['foo']

        # Check that we've written the test right
        self.assertEqual(self.g, other)

    def test_copy(self):
        other = self.g.copy()
        self.assertEqual(self.g, other)

        other.vertices[4]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.vertices[4]['foo']

        other.edges[(4, 8)]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.edges[(4, 8)]['foo']

        # Check that we've written the test right
        self.assertEqual(self.g, other)
