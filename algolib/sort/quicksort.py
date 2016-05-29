"""Quicksort with Lomuto partitioning."""


def sort(lst, start=0, stop=None):
    """In-place quicksort.

    Args:
        lst: List to sort
        start: Start index
        stop: Stop index
    """
    if stop is None:
        stop = len(lst)

    length = stop - start
    if length <= 1:
        return

    pivot = stop - 1
    j = start
    for i in xrange(start, pivot):
        if lst[i] < lst[pivot]:
            lst[i], lst[j] = lst[j], lst[i]
            j += 1

    lst[pivot], lst[j] = lst[j], lst[pivot]
    sort(lst, start, j)
    sort(lst, j + 1, stop)
