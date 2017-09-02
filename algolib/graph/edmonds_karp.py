"""Edmonds-Karp algorithm for finding maximum flow over a graph. Works on both
directed and undirected graphs.
Time complexity: O(VE^2)

For more information see Wikipedia:
https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm
"""
from collections import deque
from itertools import tee
from algolib.graph.bfs import BFS
from algolib.graph.directed import Directed


def __process_edge(graph, _dfs, source, dest, _edge):
    # Only advance over the edge if there's capacity left
    return graph[source][dest]['capacity']


def __pairwise(it):
    x, y = tee(it)
    next(y, None)
    return zip(x, y)


def __initialize_result(graph):
    # Generate a flow graph where every edge has initial flow of 0
    # and opposing edge with capacity 0. More units can flow through an edge
    # as long as capacity > 0.
    if graph.directed:
        result = graph.copy()
        # Iterate over source graph since we're changing the result that can't
        # be done while iterating and they have same edges anyway
        for x, y in graph.edges.keys():
            result.edges[(x, y)]['flow'] = 0
            if x not in result[y]:
                result.insert_edge(y, x, flow=0, capacity=0)
    else:
        result = Directed()
        for (x, y), properties in graph.edges.items():
            result.insert_edge(x, y, flow=0, capacity=properties['capacity'])
            result.insert_edge(y, x, flow=0, capacity=properties['capacity'])

    return result


def edmonds_karp(graph, source, destination):
    """Find maximum flow between two vertices in a weighted graph.

    Args:
        graph: Undirected or directed graph where every edge has property
            'capacity' that indicates how many units may flow through it.
        source: Source vertex.
        destination: Destination vertex.

    Returns:
        Tuple (flow graph, total flow) where flow graph is directed weighted
        graph that indicates the flow in the original graph. Every edge in
        the flow graph has property 'flow' which is positive integer that
        represents the flow through the edge.
    """
    result = __initialize_result(graph)

    if source == destination:
        return result, float('inf')

    total = 0
    while True:
        # Find shortest augmenting path with BFS
        bfs = BFS(result, process_edge=__process_edge)
        bfs.execute(source)

        # Generate path from BFS result
        terminate = False
        current = destination
        path = deque([current])
        while current != source:
            parent = bfs[current].parent

            # If there's no more augmenting path we're done
            if parent is None:
                terminate = True
                break

            path.appendleft(parent)
            current = parent

        if terminate:
            break

        # Find the minimum capacity along the augmenting path, that's the
        # amount of flow that can be added
        volume = min(result[x][y]['capacity'] for x, y in __pairwise(path))
        total += volume

        # Go through the path and update capacity & flow. Every time x amount
        # of flow is added to edge (u, v) (and capacity decreased) the capacity
        # of opposing edge (v, u) is added by the same amount. Note that only
        # one of the edges may contain flow at any given time
        for x, y in __pairwise(path):
            result[y][x]['capacity'] += volume
            result[x][y]['capacity'] -= volume
            if volume <= result[y][x]['flow']:
                result[y][x]['flow'] -= volume
            else:
                result[x][y]['flow'] = volume - result[y][x]['flow']
                result[y][x]['flow'] = 0

    # Sanitize the result by removing edges which don't have any flow
    remove = {edge for edge, properties in result.edges.items()
              if not properties['flow']}

    for edge in remove:
        result.remove_edge(*edge)

    return result, total
