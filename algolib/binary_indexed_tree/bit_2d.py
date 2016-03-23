"""Two dimensional binary indexed tree, supports point updates and range sum
queries. For example can be used query sum of values on M x N area in matrix.
Uses 1-based indexing so for all the operations that take index as argument 1
is the minimum value. It should also be noted that when BIT is generated the
first row and column in the given matrix will be discarded.

Time complexity of the operations:
- creation: O(mn)
- point query: O(log m * log n)
- range query: O(log m * log n)
- point update: O(log m * log n)

For more information see:
- https://www.topcoder.com/community/data-science/data-science-tutorials/
    binary-indexed-trees/#2d
"""
from algolib.binary_indexed_tree import bit


def create(matrix):
    """Transforms given matrix to two dimensional BIT.

    Args:
        matrix: Matrix to transform, note that BIT uses 1-based indexing so
            first row and column are discarded
    """
    limit_y = len(matrix)
    limit_x = len(matrix[0])

    for y in xrange(1, limit_y):
        bit.create(matrix[y])

    for x in xrange(1, limit_x):
        for y in xrange(1, limit_y):
            k = y + (y & -y)
            if k < limit_y:
                matrix[k][x] += matrix[y][x]


def query_point(tree, y, x):
    """Returns a value from given coordinate.

    Args:
        tree: BIT
        y: Y coordinate
        x: X coordinate

    Returns:
        Value in given coordinate
    """
    res = bit.query_point(tree[y], x)
    end_y = y - (y & -y)
    y -= 1

    while y != end_y:
        res -= bit.query_point(tree[y], x)
        y -= (y & -y)

    return res


def query_top_left(tree, y, x):
    """Returns sum of values in the region (1,1)-given coordinates (inclusive).

    Args:
        tree: BIT
        y: Y coordinate
        x: X coordinate

    Returns:
        Sum of values in the region
    """
    res = 0
    x_orig = x

    while y > 0:
        x = x_orig
        while x > 0:
            res += tree[y][x]
            x -= (x & -x)
        y -= (y & -y)

    return res


def query_range(tree, start_y, start_x, end_y, end_x):
    """Returns sum of values in the region bounded by the given
    coordinates (inclusive).

    Args:
        tree: BIT
        start_y: Y coordinate of the starting point
        start_x: X coordinate of the starting point
        end_y: Y coordinate of the ending point
        end_x: X coordinate of the ending point

    Returns:
        Sum of values in the region
    """
    res = 0
    start_y -= 1

    while end_y > start_y:
        res += bit.query_range(tree[end_y], start_x, end_x)
        end_y -= (end_y & -end_y)

    while start_y > end_y:
        res -= bit.query_range(tree[start_y], start_x, end_x)
        start_y -= (start_y & -start_y)

    return res


def update_point(tree, y, x, diff):
    """Updates value in given coordinate.

    Args:
        tree: BIT
        y: Y coordinate
        x: X coordinate
        diff: Difference to previous value (use query_point
            if not tracked in separate matrix)
    """
    max_y = len(tree)
    max_x = len(tree[0])
    x_orig = x

    while y < max_y:
        x = x_orig
        while x < max_x:
            tree[y][x] += diff
            x += (x & -x)
        y += (y & -y)
