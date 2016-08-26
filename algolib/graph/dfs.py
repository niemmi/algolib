"""Depth first search. Executes depth first search from given node and creates
DFS tree during the process. Behavior can be customized by providing hooks
that will be called right after vertex processing starts, when edge is processed
and right before vertex processing ends. DFS can be terminated early by raising
an exception in one of the hooks. Implementation is based on the one presented
in The Algorithm Design Manual, chapter 5.

Time complexity: O(V + E)
"""


def _hook(*_):
    """Default hook to be called in case user doesn't provide one."""
    return True


class DFS(object):
    """Depth first search which builds DFS tree and call provided hooks during
    the process.

    Attributes:
        graph: Graph on which DFS is being done on.
        _vertex: Dictionary of vertices in the graph being processed where
            vertex name is the key and value is an object representing current
            state with following attributes:
                state: Current state of the vertex.
                parent: Vertex parent in DFS tree, None if there's no parent.
                entry:  Entry time.
                exit: Exit time.
        time: Current time, incremented by 1 every time vertex is entered and
            exited.
        process_vertex_early: Hook that is called when vertex processing starts.

            hook(graph, dfs, vertex) where
                graph: The graph n which DFS is being done.
                dfs: DFS object.
                vertex: Vertex that is being processed.
        process_vertex_late: Hook that is called just before vertex is
            processing is completed.

            hook(graph, dfs, vertex) where
                graph: The graph n which DFS is being done.
                dfs: DFS object.
                vertex: Vertex that is being processed.
        process_edge: Hook that is called when edge is processed. Returns True
            if edge can be advanced, False if not.

            hook(graph, dfs, source, dest, edge):
                graph: The graph n which DFS is being done.
                dfs: DFS object.
                source: Edge start vertex.
                dest: Edge end vertex.
                edge: Edge key.
    """

    # States
    UNDISCOVERED = 0    # Vertex hasn't been seen yet
    DISCOVERED = 1      # Vertex has been seen but hasn't been processed yet
    PROCESSED = 2       # Vertex has been processed

    # Edge categories

    # Tree edge which is part of DFS tree
    TREE = 0
    # Cross edge from tree branch to another
    CROSS = 1
    # Edge pointing back from a vertex to one of it's ancestors,
    # exists only in directed graphs
    BACK = 2
    # Forward edge to a descendant that has already been processed,
    # exists only in directed graphs
    FORWARD = 3

    # This is just a simple data holder
    # pylint: disable=too-few-public-methods
    class State(object):
        """Class for representing vertex state during DFS."""
        def __init__(self):
            """Initializer, initializes default state."""
            self.state = DFS.UNDISCOVERED
            self.parent = None
            self.entry = self.exit = -1
    # pylint: enable=too-few-public-methods

    def __init__(self, graph, process_vertex_early=_hook,
                 process_vertex_late=_hook, process_edge=_hook):
        """Initializer, initializes DFS from given graph and hooks.

        Args:
            graph: Graph to perform the DFS on.
            process_vertex_early: Optional hook to be called just after vertex
                processing starts.
            process_vertex_late: Optional hook to be called right before vertex
                processing ends.
            process_edge: Optional hook to be called when edge is processed.
        """
        self.graph = graph
        self._vertex = {vertex: self.State() for vertex in graph.vertices}
        self.time = 0
        self.process_vertex_early = process_vertex_early
        self.process_vertex_late = process_vertex_late
        self.process_edge = process_edge

    def execute(self, vertex):
        """Executes DFS starting from given vertex. Note that if graph contains
        multiple components method may be called once for each. Processing can
        be terminated early by providing a hook that raises an exception.

        Args:
            vertex: Vertex to start the DFS from.

        Raises:
            Exceptions from hooks, by default nothing.
        """
        v = self[vertex]
        v.state = self.DISCOVERED
        self.time += 1
        v.entry = self.time
        self.process_vertex_early(self.graph, self, vertex)
        directed = self.graph.directed

        # Iterate over edge key, neighbor pairs
        for edge, other in self.graph.edges_from(vertex):
            n = self[other]

            if n.state == self.UNDISCOVERED:
                n.parent = vertex
                if self.process_edge(self.graph, self, vertex, other, edge):
                    self.execute(other)
            elif (n.state == self.DISCOVERED and other != v.parent) or directed:
                self.process_edge(self.graph, self, vertex, other, edge)

        self.process_vertex_late(self.graph, self, vertex)
        self.time += 1
        v.exit = self.time
        v.state = self.PROCESSED

    def edge_category(self, source, dest):
        """Categorizes a given edge, note that given return value is only valid
        when called from process_edge hook.

        Args:
            source: Source vertex.
            dest: Destination vertex.

        Returns:
            Edge category.
        """
        if self[dest].state == self.UNDISCOVERED:
            return self.TREE
        elif self[dest].state == self.DISCOVERED:
            return self.BACK
        elif self[source].entry > self[dest].entry:
            return self.CROSS
        else:
            return self.FORWARD

    def __getitem__(self, item):
        return self._vertex[item]
