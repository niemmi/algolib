"""Algorithms for finding cut vertices and cut edges from undirected graph.
Cut vertex or cut edge is a vertex or edge of which removal will disconnect
the graph. Time complexity: O(V + E)
"""
from algolib.graph.dfs import DFS


def __process_early(_graph, dfs, vertex):
    dfs[vertex].reachable_ancestor = vertex
    dfs[vertex].out_degree = 0


def __process_late_cut_vertex(_graph, dfs, vertex):
    obj = dfs[vertex]

    if obj.parent is None:
        if obj.out_degree > 1:
            # Root cut-vertex
            dfs.result.add(vertex)
        return

    parent = dfs[obj.parent]
    if parent.parent:
        if obj.reachable_ancestor == obj.parent:
            # Parent cut-vertex
            dfs.result.add(obj.parent)
        elif obj.reachable_ancestor == vertex:
            # Bridge cut-vertex
            dfs.result.add(obj.parent)
            if obj.out_degree:
                dfs.result.add(vertex)

    if dfs[obj.reachable_ancestor].entry < dfs[parent.reachable_ancestor].entry:
        parent.reachable_ancestor = obj.reachable_ancestor


def __process_late_cut_edge(_graph, dfs, vertex):
    obj = dfs[vertex]

    if obj.parent is None:
        return

    if obj.reachable_ancestor == vertex:
        dfs.result.add((obj.parent, vertex))

    parent = dfs[obj.parent]
    if dfs[obj.reachable_ancestor].entry < dfs[parent.reachable_ancestor].entry:
        parent.reachable_ancestor = obj.reachable_ancestor


def __process_edge(_graph, dfs, source, dest, _edge):
    category = dfs.edge_category(source, dest)
    if category == DFS.TREE:
        dfs[source].out_degree += 1
    elif category == DFS.BACK and dest != dfs[source].parent:
        dfs[source].reachable_ancestor = dest


def cut_vertices(graph):
    """Returns all the cut vertices in given undirected graph.

    Args:
        graph: Undirected graph.

    Returns:
        Set of cut vertices.
    """
    dfs = DFS(graph,
              process_vertex_early=__process_early,
              process_vertex_late=__process_late_cut_vertex,
              process_edge=__process_edge)
    dfs.result = set()

    for v in graph.vertices:
        obj = dfs[v]
        if obj.state == DFS.UNDISCOVERED:
            dfs.execute(v)

    return dfs.result


def cut_edges(graph):
    """Returns all the cut edges in given undirected graph.

    Args:
        graph: Undirected graph.

    Returns:
        Set of cut edges where edge is tuple consisting two edges in no
        particular order.
    """
    dfs = DFS(graph,
              process_vertex_early=__process_early,
              process_vertex_late=__process_late_cut_edge,
              process_edge=__process_edge)
    dfs.result = set()

    for v in graph.vertices:
        obj = dfs[v]
        if obj.state == DFS.UNDISCOVERED:
            dfs.execute(v)

    return dfs.result
