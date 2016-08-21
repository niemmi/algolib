"""Prim's algorithm for finding minimum spanning tree from undirected weighted
graph. Time complexity: O(V^2).

For more information see https://en.wikipedia.org/wiki/Prim%27s_algorithm.
"""


def prim(graph):
    """Finds minimum spanning tree from undirected weighted graph.

    Args:
        graph: Undirected graph where each edge has 'weight' property.

    Returns:
        List of edges in minimum spanning tree.
    """
    # Store vertices not yet in the tree to a dict
    # {vertex: [distance, closest vertex in the tree]}
    distance = {vertex: [float('inf'), None] for vertex in graph.vertices}
    edges = []

    # Start from random vertex, iterate over all vertices
    vertex = next(iter(graph.vertices), None)
    while vertex is not None:
        del distance[vertex]
        min_vertex = None
        min_dist = float('inf')

        # Iterate over unconnected vertices
        for other in distance:
            # Update ones that are connected to selected vertex
            if other in graph[vertex]:
                weight = graph[vertex][other]['weight']
                if weight < distance[other][0]:
                    distance[other] = [weight, vertex]

            # Find unconnected vertex with minimum distance to process next
            if distance[other][0] < min_dist:
                min_vertex = other
                min_dist = distance[other][0]

        vertex = min_vertex

        # If there's next vertex to process add edge connecting it to tree
        if vertex:
            edges.append([vertex, distance[vertex][1]])

    return edges
