"""Prim's algorithm for finding minimum spanning tree from undirected weighted
graph. Time complexity: O(E log V).

For more information see https://en.wikipedia.org/wiki/Prim%27s_algorithm.
"""
from algolib.priority_queue import PriorityQueue


def prim(graph, queue_constructor=PriorityQueue):
    """Finds minimum spanning tree from undirected weighted graph.

    Args:
        graph: Undirected graph where each edge has 'weight' property.
        queue_constructor: Optional argument used to construct priority queue,
            must satisfy following requirements:
            - Accepts iterable of (priority, key) tuples as argument.
            - Returned object must support pop() that returns (priority, key)
                tuple that has minimum priority, in case multiple keys have
                same priority any of them will do.
            - Returned object must support change_priority(priority, key) that
                will change the priority of existing key.
            - Returned object must evaluate True in boolean context in case it
                contains items and False if it's empty.

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
    queue = queue_constructor((float('inf'), vertex)
                              for vertex in graph.vertices)
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
