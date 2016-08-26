"""Tests if graph is bipartite, time complexity: O(V + E)."""
from algolib.graph.bfs import BFS

# Vertex colors in bipartite graph
UNCOLORED = -1
WHITE = 0
BLACK = 1


def __process_edge(_graph, bfs, source, dest, _edge):
    if bfs.color[source] == bfs.color[dest]:
        bfs.bipartite = False
        raise StopIteration

    bfs.color[dest] = int(not bfs.color[source])
    return True

def bipartite(graph):
    """Checks if given graph is bipartite.

    Args:
        graph: Graph to check/

    Returns:
        True if graph is bipartite, False if not.
    """
    bfs = BFS(graph, process_edge=__process_edge)
    bfs.color = {vertex: UNCOLORED for vertex in graph.vertices}
    bfs.bipartite = True

    try:
        for vertex in graph.vertices:
            if bfs.color[vertex] == UNCOLORED:
                bfs.color[vertex] = WHITE
                bfs.execute(vertex)
    except StopIteration:
        pass

    return bfs.bipartite
