"""Heap sort."""


def bubble_down(lst, length, index):
    """Moves number in max-priority_queue down to its' correct place.

    Args:
        lst: List
        length: List length
        index: Index of number to move
    """
    max_index = index
    for i in range(index * 2 + 1, min(length, index * 2 + 3)):
        if lst[i] > lst[max_index]:
            max_index = i

    if max_index != index:
        lst[index], lst[max_index] = lst[max_index], lst[index]
        bubble_down(lst, length, max_index)


def sort(lst):
    """In-place heapsort, O(n log n) time complexity

    Args:
        lst: List to sort
    """
    length = len(lst)

    # Heapify, O(n) time complexity
    for i in range((length - 1) // 2, -1, -1):
        bubble_down(lst, length, i)

    # Extract max, swap to end, O(n log n) time complexity
    for i in range(length - 1, 0, -1):
        lst[0], lst[i] = lst[i], lst[0]
        bubble_down(lst, i, 0)
