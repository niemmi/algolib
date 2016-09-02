"""Dijkstra's algorithm for finding shortest path between vertices in weighted
graph. Works both with directed and undirected graphs as long as all the edges
have a property called 'weight'.

Time complexity: O(E log V)
"""
from algolib.priority_queue import PriorityQueue


def dijkstra(graph, source, target=None, queue_constructor=PriorityQueue):
    """Dijkstra's algorithm that finds minimum distance from given vertex.

    Args:
        graph: Graph where every edge has 'weight' property.
        source: Vertex to star from.
        target: Optional target vertex, if not given distance to every vertex
            reachable from source is calculated.
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
        Dictionary where vertices are keys and values are [distance, parent]
        pairs.
    """
    queue = queue_constructor((float('inf'), vertex)
                              for vertex in graph.vertices)
    result = {vertex: [float('inf'), None] for vertex in graph.vertices}
    queue.change_priority(0, source)
    result[source][0] = 0

    while queue and source != target:
        distance, source = queue.pop()

        # Graph is disconnected
        if distance == float('inf'):
            break

        for other in graph[source]:
            distance_to_other = distance + graph[source][other]['weight']
            if distance_to_other < result[other][0]:
                queue.change_priority(distance_to_other, other)
                result[other] = [distance_to_other, source]

    return result


def dijkstra_path(dijkstra_result, source, target):
    """Constructs a path from a distance map returned by Dijkstra's algorithm.

    Args:
        dijkstra_result: Distance map from Dijkstra's algorithm.
        source: Vertex to start path from.
        target: Vertex to end the path.

    Returns:
        List of vertices covering path from source to target, both ends
        included. If target vertex is not reachable from source then None
        is returned.
    """
    result = [target]
    while True:
        if target is None:
            return None

        if target == source:
            return result[::-1]

        target = dijkstra_result[target][1]
        result.append(target)
