"""Topological sort for directed acyclic graphs, time complexity: O(E + V)."""
from algolib.graph.dfs import DFS


def __process_vertex_late(_dag, dfs, vertex):
    dfs.res.append(vertex)


def __process_edge(_dag, dfs, source, dest, _edge):
    category = dfs.edge_category(source, dest)
    if category == DFS.BACK:
        raise StopIteration

    return True


def top_sort(dag):
    """Topological sort.

    Args:
        dag: Directed graph

    Returns:
        List of vertices in topologically sorted order or None in case that
        graph contains a cycle.
    """
    dfs = DFS(dag, process_vertex_late=__process_vertex_late,
              process_edge=__process_edge)
    dfs.res = []
    try:
        for vertex in dag.vertices:
            if dfs[vertex].state == DFS.UNDISCOVERED:
                dfs.execute(vertex)

        return dfs.res[::-1]
    except StopIteration:
        return None
