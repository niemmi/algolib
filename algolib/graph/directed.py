"""Directed graph that doesn't have multi-edges but may contain loops.
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


class Directed(object):
    """Directed graph which may contain loops but not multiple edges.

    Attributes:
        vertices: Dictionary of vertices where keys are vertex names and
            values are dictionary of vertex properties.
        edges: Dictionary of edges where keys are tuples of vertex pairs
            (from, to) and values are dictionary of edge properties.
        _outgoing: Three level dictionary of outgoing edges where the first
            level key is source vertex, second level key is destination vertex
            and third level is edge properties.
        incoming: Three level dictionary of incoming edges where the first
            level key is destination vertex, second level key is source vertex
            and third level is edge properties.
    """

    def __init__(self):
        """Initializer, initializes empty graph."""
        self.vertices = {}
        self.edges = {}
        self._outgoing = defaultdict(dict)
        self.incoming = defaultdict(dict)

    @property
    def directed(self):
        """Returns boolean value telling if graph is directed or not.

        Returns:
            Always True.
        """
        return True

    def insert_vertex(self, name, **kwargs):
        """Inserts vertex to graph.

        Args:
            name: Vertex name, any hashable object
            **kwargs: Optional properties, if vertex already exists then given
                properties will be used to update existing ones.
        """
        kwargs.update(self.vertices.get(name, {}))
        self.vertices[name] = kwargs
        self._outgoing.setdefault(name, {})
        self.incoming.setdefault(name, {})

    def remove_vertex(self, name):
        """Removes vertex from graph. Removes also all the edges the vertex
        is part of.

        Args:
            name: Name of the vertex.
        """
        del self.vertices[name]

        # Remove edges without copying the keys
        while self._outgoing[name]:
            self.remove_edge(name, next(iter(self._outgoing[name])))

        while self.incoming[name]:
            self.remove_edge(next(iter(self.incoming[name])), name)

        del self._outgoing[name]
        del self.incoming[name]

    def insert_edge(self, source, dest, **kwargs):
        """Inserts edge to graph. If vertices don't exist they are created.

        Args:
            source: Source vertex.
            dest: Destination vertex.
            **kwargs: Optional properties for the edge
        """
        self.vertices.setdefault(source, {})
        self.vertices.setdefault(dest, {})

        kwargs.update(self.edges.get((source, dest), {}))
        self._outgoing[source][dest] = kwargs
        self.incoming[dest][source] = kwargs
        self.edges[(source, dest)] = kwargs

    def remove_edge(self, source, dest):
        """Removes edge from graph.

        Args:
            source: Source vertex.
            dest: Destination vertex.
        """
        del self.edges[(source, dest)]
        del self._outgoing[source][dest]
        del self.incoming[dest][source]

    def connected(self, source, dest):
        """Returns boolean value telling if given vertices are connected by
        an edge.

        Args:
            source: Source vertex.
            dest: Destination vertex.

        Returns:
            True if vertices are connected by edge, False if not
        """
        return (source, dest) in self.edges

    def edges_between(self, source, dest):
        """Returns iterator iterating over edges between given nodes. Note that
        with graph like this which doesn't allow multiple edges between the same
        nodes this doesn't make much sense but if multi-edge graphs are
        supported then easier to expose similar interface.

        Args:
            source: First vertex.
            dest: Second vertex.

        Returns:
            Iterator iterating over all the edges between given vertices.
        """
        if dest in self._outgoing[source]:
            yield (source, dest)

    def edges_from(self, vertex):
        """Returns iterator iterating over all the outgoing edges of given
        vertex.

        Args:
            vertex: Edge start vertex..

        Returns:
            Iterator iterating over all the outgoing edges of given vertex.
            Iterator returns (edge key, destination vertex) tuples where edge
            key can be used to index Undirected.edges.
        """
        for neighbor in self._outgoing[vertex]:
            yield (vertex, neighbor), neighbor

    def __getitem__(self, item):
        return self._outgoing[item]

    def degree_in(self, vertex):
        """Returns in degree of given vertex.

        Args:
            vertex: Vertex.

        Returns:
            In degree.
        """
        return len(self.incoming[vertex])

    def degree_out(self, vertex):
        """Returns out degree of given vertex.

        Args:
            vertex: Vertex.

        Returns:
            Out degree.
        """
        return len(self._outgoing[vertex])

    def __eq__(self, other):
        return isinstance(other, Directed) and \
               self.edges == other.edges and \
               self.vertices == other.vertices

    def __ne__(self, other):
        return not self == other

    def __copy__(self):
        other = Directed()
        for vertex, properties in self.vertices.items():
            other.insert_vertex(vertex, **properties)

        for (x, y), properties in self.edges.items():
            other.insert_edge(x, y, **properties)

        return other

    copy = __copy__
