"""Kruskal's algorithm for finding minimum spanning tree from undirected
weighted graph. For sparse graphs the algorithm is faster than Prim's.
Time complexity: O(E log E) which comes from sorting the edges at the
beginning.
"""
from algolib.disjoint_set import DisjointSet


def kruskal(graph):
    """Find minimum spanning tree from undirected weighted graph.

    Args:
        graph: Undirected graph where each edge has 'weight' property.

    Returns:
        List of edges in minimum spanning tree.
    """
    edges = sorted(graph.edges, key=lambda x: graph[x[0]][x[1]]['weight'])
    components = DisjointSet(graph.vertices)
    result = []

    for edge in edges:
        if not components.same_component(*edge):
            components.union(*edge)
            result.append(edge)

    return result
