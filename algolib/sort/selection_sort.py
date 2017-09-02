"""Selection sort."""


def sort(lst):
    """In-place selection sort

    Args:
        lst: List to sort
    """
    for i in range(len(lst) - 1):
        min_index = i
        for j in range(i + 1, len(lst)):
            if lst[min_index] > lst[j]:
                min_index = j
        lst[min_index], lst[i] = lst[i], lst[min_index]
