"""Insertion sort."""


def sort(lst):
    """In-place insertion sort.

    Args:
        lst: List to sort
    """
    for i in range(1, len(lst)):
        for j in range(i, 0, -1):
            if lst[j - 1] <= lst[j]:
                break
            lst[j - 1], lst[j] = lst[j], lst[j - 1]
