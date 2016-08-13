"""Undirected graph that doesn't have multi-edges but may contain loops.
Both vertices and edges may have associated properties. Vertices as stored
as an adjacency matrix using dicts and as a separate dict that maybe iterated
over.

Time complexity of the operations:
- check if edge (x, y) exists: O(1)
- check degree of vertex: O(1)
- insert/delete edge: O(1)
- insert vertex: O(1)
- delete vertex: O(number of connected edges)
- iterate vertices/edges: O(n)

Interface is loosely based on NetworkX (http://networkx.github.io/).
"""
from collections import defaultdict


class Undirected(object):
    """Undirected graph which may contain loops but not multiple edges.

    Attributes:
        vertices: Dictionary of vertices where keys are vertex names and
            values are dictionary of vertex properties.
        edges: Dictionary of edges where keys are tuples of vertex pairs in
            sorted order and values are dictionary of edge properties.
        _neighbors: Three level dictionary where first level keys are vertices,
            second level keys are neighboring vertices and third level is
            edge properties. Use index operator to access edges.
    """

    def __init__(self):
        """Initializer, initializes empty graph."""
        self.vertices = {}
        self.edges = {}
        self._neighbors = defaultdict(dict)

    @property
    def directed(self):
        """Returns boolean value telling if graph is directed or not.

        Returns:
            Always False.
        """
        return False

    @staticmethod
    def __key(x, y):
        # Note that on Python 3 frozenset would be better option
        return tuple(sorted([x, y]))

    def insert_vertex(self, name, **kwargs):
        """Inserts vertex to graph.

        Args:
            name: Vertex name, any hashable object
            **kwargs: Optional properties, if vertex already exists then given
                properties will be used to update existing ones.
        """
        kwargs.update(self.vertices.get(name, {}))
        self.vertices[name] = kwargs
        self._neighbors.setdefault(name, {})

    def remove_vertex(self, name):
        """Removes vertex from graph. Removes also all the edges the vertex
        is part of.

        Args:
            name: Name of the vertex.
        """
        del self.vertices[name]

        # Iterate over neighbors without copying
        while self._neighbors[name]:
            self.remove_edge(name, next(iter(self._neighbors[name])))

        del self._neighbors[name]

    def insert_edge(self, x, y, **kwargs):
        """Inserts edge to graph. If vertices don't exist they are created.

        Args:
            x: First vertex.
            y: Second vertex.
            **kwargs: Optional properties for the edge
        """
        self.vertices.setdefault(x, {})
        self.vertices.setdefault(y, {})

        edge_key = self.__key(x, y)
        kwargs.update(self.edges.get(edge_key, {}))
        self._neighbors[x][y] = kwargs
        self._neighbors[y][x] = kwargs
        self.edges[edge_key] = kwargs

    def remove_edge(self, x, y):
        """Removes edge from vertex.

        Args:
            x: First vertex.
            y: Second vertex.
        """
        del self.edges[self.__key(x, y)]
        del self._neighbors[x][y]

        if x != y:
            del self._neighbors[y][x]

    def connected(self, x, y):
        """Returns boolean value telling if given vertices are connected by
        an edge.

        Args:
            x: First vertex.
            y: Second vertex.

        Returns:
            True if vertices are connected by edge, False if not
        """
        return self.__key(x, y) in self.edges

    def edges_between(self, x, y):
        """Returns iterator iterating over edges between given nodes. Note that
        with graph like this which doesn't allow multiple edges between the same
        nodes this doesn't make much sense but if multi-edge graphs are
        supported then easier to expose similar interface.

        Args:
            x: First vertex.
            y: Second vertex.

        Returns:
            Iterator iterating over all the edges between given vertices.
        """
        if y in self._neighbors[x]:
            yield self.__key(x, y)

    def edges_from(self, vertex):
        """Returns iterator iterating over all the edges connected to given
        vertex.

        Args:
            vertex: Edge endpoint.

        Returns:
            Iterator iterating over all the edges connecting given vertex.
            Iterator returns (edge key, connected vertex) tuples where edge key
            can be used to index Undirected.edges.
        """
        for neighbor in self._neighbors[vertex]:
            yield self.__key(vertex, neighbor), neighbor

    def __getitem__(self, item):
        return self._neighbors[item]

    def degree(self, vertex):
        """Returns degree of given vertex.

        Args:
            vertex: Vertex who's degree is queried.

        Returns:
            Vertex degree, note that if vertex has a loop it is considered
            as degree of 2.
        """
        loop = vertex in self._neighbors[vertex]
        return len(self._neighbors[vertex]) + loop

    def __eq__(self, other):
        return isinstance(other, Undirected) and \
               self.edges == other.edges and \
               self.vertices == other.vertices

    def __ne__(self, other):
        return not self == other

    def __copy__(self):
        copy = Undirected()
        for vertex, data in self.vertices.iteritems():
            copy.insert_vertex(vertex, **data)
        for (x, y), data in self.edges.iteritems():
            copy.insert_edge(x, y, **data)

        return copy

    copy = __copy__
