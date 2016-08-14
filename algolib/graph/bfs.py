"""Breadth first search. Executes breadth first search from given node and
creates BFS tree during the process. Behavior can be customized by providing
hooks that will be called right after vertex processing starts, when edge is
processed and right before vertex processing ends. BFS can be terminated early
by raising an exception in one of the hooks. Implementation is based on the one
presented in The Algorithm Design Manual, chapter 5.

Time complexity: O(V + E)
"""
from collections import deque


def _hook(*_):
    """Default hook to be called in case user doesn't provide one."""
    pass

# Single algorithm, can't be that many public methods
# pylint: disable=too-few-public-methods
class BFS(object):
    """Breadth first search which builds BFS tree and call provided hooks during
    the process.

    Attributes:
        graph: Graph on which DFS is being done on.
        _vertex: Dictionary of vertices in the graph being processed where
            vertex name is the key and value is an object representing current
            state with following attributes:
                state: Current state of the vertex.
                parent: Vertex parent in BFS tree, None if there's no parent.
        process_vertex_early: Hook that is called when vertex processing starts.

            hook(graph, dbs, vertex) where
                graph: The graph n which BFS is being done.
                bfs: BFS object.
                vertex: Vertex that is being processed.
        process_vertex_late: Hook that is called just before vertex is
            processing is completed.

            hook(graph, bfs, vertex) where
                graph: The graph n which BFS is being done.
                bfs: BFS object.
                vertex: Vertex that is being processed.
        process_edge: Hook that is called when edge is processed.

            hook(graph, bfs, source, dest, edge):
                graph: The graph n which BFS is being done.
                bfs: BFS object.
                source: Edge start vertex.
                dest: Edge end vertex.
                edge: Edge key.
    """

    # States
    UNDISCOVERED = 0    # Vertex hasn't been seen yet
    DISCOVERED = 1      # Vertex has been seen but hasn't been processed yet
    PROCESSED = 2       # Vertex has been processed

    class State(object):
        """Class for representing vertex state during BFS."""
        def __init__(self):
            """Initializer, initializes default state."""
            self.state = BFS.UNDISCOVERED
            self.parent = None

    def __init__(self, graph, process_vertex_early=_hook,
                 process_vertex_late=_hook, process_edge=_hook):
        """Initializer, initializes BFS from given graph and hooks.

        Args:
            graph: Graph to perform the BFS on.
            process_vertex_early: Optional hook to be called just after vertex
                processing starts.
            process_vertex_late: Optional hook to be called right before vertex
                processing ends.
            process_edge: Optional hook to be called when edge is processed.
        """
        self.graph = graph
        self._vertex = {vertex: self.State() for vertex in graph.vertices}
        self.process_vertex_early = process_vertex_early
        self.process_vertex_late = process_vertex_late
        self.process_edge = process_edge

    def execute(self, vertex):
        """Executes BFS starting from given vertex. Note that if graph contains
        multiple components method may be called once for each. Processing can
        be terminated early by providing a hook that raises an exception.

        Args:
            vertex: Vertex to start the BFS from.

        Raises:
            Exceptions from hooks, by default nothing.
        """
        self[vertex].state = self.DISCOVERED
        que = deque([vertex])
        while que:
            vertex = que.popleft()
            self.process_vertex_early(self.graph, self, vertex)
            self[vertex].state = self.PROCESSED
            for edge, other in self.graph.edges_from(vertex):
                obj = self[other]
                if obj.state != self.PROCESSED or self.graph.directed:
                    self.process_edge(self.graph, self, vertex, other, edge)
                if obj.state == self.UNDISCOVERED:
                    obj.state = self.DISCOVERED
                    obj.parent = vertex
                    que.append(other)
            self.process_vertex_late(self.graph, self, vertex)

    def __getitem__(self, item):
        return self._vertex[item]

# pylint: enable=too-few-public-methods
