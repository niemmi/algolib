import unittest
from .context import Directed
from collections import Counter

EDGES = [
    [0, 1],
    [0, 2],
    [0, 4],
    [1, 1],
    [1, 3],
    [1, 4],
    [2, 1],
    [3, 0]
]


class TestDirected(unittest.TestCase):
    @staticmethod
    def initialize_graph():
        graph = Directed()
        for x, y in EDGES:
            graph.insert_edge(x, y)

        return graph

    def setUp(self):
        self.g = self.initialize_graph()

    def test_insert_vertex_adds_vertex(self):
        self.assertNotIn(5, self.g.vertices)
        self.g.insert_vertex(5)
        self.assertIn(5, self.g.vertices)

    def test_insert_vertex_takes_kwargs(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_vertex(5, **kwargs)
        self.assertEqual(kwargs, self.g.vertices[5])

    def test_insert_vertex_doesnt_override_existing_edges(self):
        # Degrees not needed because they're equal to len(incoming/outgoing)
        outgoing = set(self.g._outgoing[1].keys())
        incoming = set(self.g.incoming[1].keys())
        self.g.insert_vertex(1)
        self.assertEqual(outgoing, self.g._outgoing[1].viewkeys())
        self.assertEqual(incoming, self.g.incoming[1].viewkeys())

    def test_insert_vertex_doesnt_override_existing_properties(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_vertex(5, **kwargs)
        kwargs2 = {'bar': 'foo'}
        self.g.insert_vertex(5, **kwargs2)
        kwargs.update(kwargs2)

        self.assertEqual(kwargs, self.g.vertices[5])

    def test_remove_vertex_removes_vertex(self):
        for v in self.g.vertices.keys():
            self.g.remove_vertex(v)
            self.assertNotIn(v, self.g.vertices)

    def test_remove_vertex_removes_edges(self):
        self.g.remove_vertex(1)

        self.assertNotIn(1, self.g._outgoing)
        self.assertNotIn(1, self.g.incoming)

        for v in self.g.vertices:
            self.assertNotIn(1, self.g[v])
            self.assertNotIn(1, self.g.incoming[v])

        for e in self.g.edges:
            self.assertNotIn(1, e)

    def test_remove_vertex_removes_properties(self):
        self.g.insert_vertex(5, foo='bar')
        self.g.remove_vertex(5)
        self.g.insert_vertex(5)

        self.assertEqual({}, self.g.vertices[5])

    def test_insert_edge_adds_edge(self):
        self.assertNotIn((3, 4), self.g.edges)
        self.g.insert_edge(3, 4)

        self.assertIn((3, 4), self.g.edges)
        self.assertIn(4, self.g[3])
        self.assertIn(3, self.g.incoming[4])

    def test_insert_edge_takes_kwargs(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_edge(3, 4, **kwargs)

        self.assertEqual(kwargs, self.g.edges[(3, 4)])
        self.assertEqual(kwargs, self.g[3][4])
        self.assertEqual(kwargs, self.g.incoming[4][3])

    def test_insert_edge_doesnt_override_existing(self):
        kwargs = {'foo': 'bar'}
        self.g.insert_edge(3, 4, **kwargs)
        kwargs2 = {'bar': 'foo'}
        self.g.insert_edge(3, 4, **kwargs2)
        kwargs.update(kwargs2)

        self.assertEqual(kwargs, self.g.edges[(3, 4)])
        self.assertEqual(kwargs, self.g[3][4])
        self.assertEqual(kwargs, self.g.incoming[4][3])

    def test_remove_edge_removes_properties(self):
        self.g.insert_edge(3, 4, foo='bar')
        self.g.remove_edge(3, 4)
        self.g.insert_edge(3, 4)

        self.assertEqual({}, self.g.edges[(3, 4)])
        self.assertEqual({}, self.g[3][4])
        self.assertEqual({}, self.g.incoming[4][3])

    def test_connected(self):
        for x in self.g.vertices:
            for y in self.g.vertices:
                self.assertEqual([x, y] in EDGES, self.g.connected(x, y))

    def test_edges_between(self):
        for x in self.g.vertices:
            for y in self.g.vertices:
                l = list(self.g.edges_between(x, y))
                self.assertEqual([x, y] in EDGES, len(l))
                if l:
                    self.assertEqual((x, y), l[0])

    def test_edges_from(self):
        edges = set(tuple(e) for e in EDGES)
        for v in self.g.vertices:
            edges.difference_update(e for e, _ in self.g.edges_from(v))

        self.assertEqual(next(self.g.edges_from(3)), ((3, 0), 0))

    def test_degree_in(self):
        c = Counter(v for _, v in EDGES)
        for v in c:
            self.assertEqual(c[v], self.g.degree_in(v))

    def test_degree_out(self):
        c = Counter(v for v, _ in EDGES)
        for v in c:
            self.assertEqual(c[v], self.g.degree_out(v))

    def test_eq(self):
        other = self.initialize_graph()
        self.assertEqual(self.g, other)

        other.insert_vertex(5)
        self.assertNotEqual(self.g, other)
        other.remove_vertex(5)

        other.vertices[4]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.vertices[4]['foo']

        other.insert_edge(3, 4)
        self.assertNotEqual(self.g, other)
        other.remove_edge(3, 4)

        other.edges[(1, 3)]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.edges[(1, 3)]['foo']

        # Check that we've written the test right
        self.assertEqual(self.g, other)

    def test_copy(self):
        other = self.g.copy()
        self.assertEqual(self.g, other)

        other.vertices[4]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.vertices[4]['foo']

        other.edges[(1, 3)]['foo'] = 'bar'
        self.assertNotEqual(self.g, other)
        del other.edges[(1, 3)]['foo']

        # Check that we've written the test right
        self.assertEqual(self.g, other)
