"""Algorithm for finding strongly connected components from a directed graph.
Component is strongly connected when there's a path from every vertex in to
every other vertex within the component.
Time complexity: O(V + E)
"""
from collections import defaultdict
from algolib.graph.dfs import DFS


def __process_vertex_early(_graph, dfs, vertex):
    dfs.stack.append(vertex)


def __process_vertex_late(_graph, dfs, vertex):
    obj = dfs[vertex]

    if obj.low == vertex:
        while True:
            top = dfs.stack.pop()
            dfs[top].component = dfs.index
            dfs.result[dfs.index].append(top)
            if top == vertex:
                break

        dfs.index += 1

    if obj.parent and dfs[obj.low].entry < dfs[dfs[obj.parent].low].entry:
        dfs[obj.parent].low = obj.low


def __process_edge(_graph, dfs, source, dest, _edge):
    cat = dfs.edge_category(source, dest)
    src = dfs[source]
    dst = dfs[dest]

    if cat == DFS.BACK or (cat == DFS.CROSS and dst.component is None):
        if dst.entry < dfs[src.low].entry:
            src.low = dest

    return True


def strong_components(graph):
    """Finds strongly connected components from given directed graph.

    Args:
        graph: Directed graph.

    Returns:
        List of components where each component is a list of vertices in
        that component. Components and vertices within a component are in
        no particular order.
    """
    dfs = DFS(graph,
              process_vertex_early=__process_vertex_early,
              process_vertex_late=__process_vertex_late,
              process_edge=__process_edge)

    # Current component index
    dfs.index = 0

    # Stack to store visited components
    dfs.stack = []

    # Result dictionary
    dfs.result = defaultdict(list)

    for vertex in graph.vertices:
        # First visited vertex in current component
        dfs[vertex].low = vertex
        # Component number
        dfs[vertex].component = None

    for vertex in graph.vertices:
        if dfs[vertex].state == DFS.UNDISCOVERED:
            dfs.execute(vertex)

    return dfs.result.values()
