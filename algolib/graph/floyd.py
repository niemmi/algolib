"""Floyd-Warshall algorithm for finding shortest path between all vertices in
a graph. Works both undirected and directed graphs as long as all edges have
property 'weight'. The only limitation is that graph may not contain negative
cycles so undirected graphs with negative weights are not allowed.

Time complexity: O(V^3)

For more information see Wikipedia:
https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
"""


def floyd(graph):
    """Floyd-Warshall algorithm for finding shortest path between all vertices
    in a weighted graph.

    Args:
        graph: Weighted graph, directed or undirected but may not contain
            negative cycles.

    Returns:
        Dictionary of dictionaries where d[source][dest] is distance between
        two vertices. In case there's no path between vertices the distance
        is float('inf').
    """
    default = {'weight': float('inf')}
    res = {x: {y: graph[x].get(y, default)['weight'] if x != y else 0
               for y in graph.vertices}
           for x in graph.vertices}

    for k in graph.vertices:
        for i in graph.vertices:
            for j in graph.vertices:
                res[i][j] = min(res[i][j], res[i][k] + res[k][j])

    return res
