"""Prim's algorithm for finding minimum spanning tree from undirected weighted
graph. Time complexity: O(E log V).

For more information see https://en.wikipedia.org/wiki/Prim%27s_algorithm.
"""
from algolib.priority_queue import PriorityQueue


def prim(graph):
    """Finds minimum spanning tree from undirected weighted graph.

    Args:
        graph: Undirected graph where each edge has 'weight' property.

    Returns:
        List of edges in minimum spanning tree.
    """
    if not graph.vertices:
        return []

    # Edges of result MST
    edges = []

    # Store vertices not yet in the tree to a dict
    # {vertex: [distance, closest vertex in the tree]}
    distances = {vertex: [float('inf'), None] for vertex in graph.vertices}

    # Store vertex, distance pairs to min priority_queue prioritized by distance
    # and mark one of the vertices as start vertex
    queue = PriorityQueue((float('inf'), vertex) for vertex in graph.vertices)
    queue.change_priority(0, next(iter(graph.vertices)))

    while queue:
        weight, vertex = queue.pop()

        # If there's a vertex that can't be reached it means that graph
        # is not connected
        if weight == float('inf'):
            raise ValueError('Graph is not connected')

        # Pop vertex off from parent map and add edge to it to result MST
        # in case that it wasn't first vertex to process
        _, parent = distances.pop(vertex)
        if parent is not None:
            edges.append([parent, vertex])

        # Update distance to all the neighboring vertices if required
        for other in graph[vertex]:
            weight = graph[vertex][other]['weight']

            if weight < distances.get(other, (-float('inf'), None))[0]:
                distances[other] = (weight, vertex)
                queue.change_priority(weight, other)

    return edges
