"""Binary indexed tree, supports point updates and range sum queries
in O(log n) time. Note that BIT uses 1-based indexing so for all the
operations that take index as argument 1 is the minimum value. It should also
be noted that when BIT is generated the first item in the given sequence is
discarded.

Time complexity of the operations:
- creation: O(n)
- point query: O(log n)
- range query: O(log n)
- point update O(log n)

For more information about binary indexed trees see:
- https://en.wikipedia.org/wiki/Fenwick_tree
- https://www.topcoder.com/community/data-science/data-science-tutorials/binary-indexed-trees/
"""
from math import log


def create(seq):
    """Transforms given sequence of numbers to BIT.

    Args:
        seq: Sequence of numbers, note that BIT uses 1-based indexing
            so seq[0] is not considered.
    """
    limit = len(seq)
    for i in range(1, limit):
        j = i + (i & -i)
        if j < limit:
            seq[j] += seq[i]


def query_point(tree, index):
    """Returns a value from given index.

    Args:
        tree: BIT
        index: Index of the value to return

    Returns:
        Value in given index
    """
    res = tree[index]
    end = index - (index & -index)
    index -= 1

    while index != end:
        res -= tree[index]
        index -= (index & -index)

    return res


def query_left(tree, index):
    """Returns sum of values between 1-index inclusive.

    Args:
        tree: BIT
        index: Last index to include to the sum

    Returns:
        Sum of values up to given index
    """
    res = 0

    while index:
        res += tree[index]
        index -= (index & -index)

    return res


def query_range(tree, start, end):
    """Returns sum of values between start-end inclusive.

    Args:
        tree: BIT
        start: First index to include to the sum
        end: Last index to include to the sum

    Returns:
        Sum of values within given range
    """
    res = 0
    start -= 1

    while end > start:
        res += tree[end]
        end -= (end & -end)

    while start > end:
        res -= tree[start]
        start -= (start & -start)

    return res


def update_point(tree, index, diff):
    """Updates value in given index.

    Args:
        tree: BIT
        index: Index to update
        diff: Difference to previous value (use query_point
            if not tracked in separate list)
    """
    end = len(tree)

    while index < end:
        tree[index] += diff
        index += (index & -index)


def contains(tree, running_sum):
    """Returns boolean value telling if given sum of values exists in BIT.

    Args:
        tree: BIT
        running_sum: Sum of values

    Returns:
        True if sum of values from beginning exists in BIT, False if not
        Example:
            tree = [0, 1, 2, 3]
            bit.create(tree)
            bit.contains(tree, 6) -> True
            bit.contains(tree, 5) -> False
    """
    index = 0
    end = len(tree)
    mask = 1 << int(log(end, 2))

    while mask and index < end:
        mid = index + mask
        if mid < end:
            if running_sum == tree[mid]:
                return True
            elif running_sum > tree[mid]:
                index = mid
                running_sum -= tree[mid]

        mask >>= 1

    return running_sum == 0 < index


def bisect_left(tree, running_sum):
    """Returns left-most index where running sum is equal or greater
    than given number.

    Args:
        tree: BIT
        running_sum: Running sum

    Returns:
        Left-most index where running sum is equal or greater than given number.
        If number is greater running sum of all items in BIT len(tree) is
        returned instead.

        Example:
            tree = [0, 1, 2, 3]
            bit.create(a)
            bit.bisect_left(tree, 1) -> 1
            bit.bisect_left(tree, 10) -> 4
            bit.bisect_left(tree, 0) -> 1
    """
    index = 0
    end = len(tree)
    mask = 1 << int(log(end, 2))

    while mask and index < end:
        mid = index + mask
        if mid < end:
            if running_sum > tree[mid]:
                index = mid
                running_sum -= tree[mid]

        mask >>= 1

    return index + 1


def bisect_right(tree, running_sum):
    """Returns left-most index where running sum is greater than given value.

    Args:
        tree: BIT
        running_sum: Running sum

    Returns:
        Left-most index where running sum is greater than given value.
        If number is greater running sum of all items in BIT len(tree) is
        returned instead.

        Example:
            tree = [0, 1, 0, 1]
            bit.create([0, 1, 0, 1])
            bit.bisect_right(tree, 1) -> 3
            bit.bisect_right(tree, 2) -> 4
            bit.bisect_right(tree, 0) -> 1
    """
    i = 0
    end = len(tree)
    mask = 1 << int(log(end, 2))

    while mask and i < end:
        mid = i + mask
        if mid < end:
            if running_sum >= tree[mid]:
                i = mid
                running_sum -= tree[mid]

        mask >>= 1

    return i + 1
