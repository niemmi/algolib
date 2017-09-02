"""Two different implementations of merge sort. First one is the standard sort
that creates the result to new list on each level. Second one is an in-place
sort that uses two alternating buffers and offsets to limit memory usage
to O(2n).
"""


def sort(lst):
    """Standard merge sort.

    Args:
        lst: List to sort

    Returns:
        Sorted copy of the list
    """
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    low = sort(lst[:mid])
    high = sort(lst[mid:])

    res = []
    i = j = 0
    while i < len(low) and j < len(high):
        if low[i] < high[j]:
            res.append(low[i])
            i += 1
        else:
            res.append(high[j])
            j += 1

    res.extend(low[i:])
    res.extend(high[j:])

    return res


def helper(lst, buf, start, stop, to_buf):
    """Helper function for in-place sort with alternating buffers.

    Args:
        lst: List to sort
        buf: Buffer to store the results
        start: Start index
        stop: Stop index
        to_buf: Boolean flag telling where result should be written to.
            In case of True result should be written to buf, if False then
            result should be written to l.
    """
    length = stop - start
    if length <= 1:
        if to_buf and length == 1:
            buf[start] = lst[start]
        return

    mid = start + length // 2
    helper(lst, buf, start, mid, not to_buf)
    helper(lst, buf, mid, stop, not to_buf)

    # If result goes to buf swap l & buf since following code will write
    # from buf to result
    if to_buf:
        lst, buf = buf, lst

    i = start
    j = mid
    to = start

    while i < mid and j < stop:
        if buf[i] < buf[j]:
            lst[to] = buf[i]
            i += 1
        else:
            lst[to] = buf[j]
            j += 1

        to += 1

    for i in range(i, mid):
        lst[to] = buf[i]
        to += 1

    for j in range(j, stop):
        lst[to] = buf[j]
        to += 1


def sort_in_place(lst):
    """In-place merge sort.

    Args:
        lst: List to sort
    """
    helper(lst, [None] * len(lst), 0, len(lst), False)
