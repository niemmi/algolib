"""Parallel sort that runs on multiple cores."""
import multiprocessing
import random
import time


def chunk(seq, count):
    """Splits given sequence to n chunks as evenly as possible.

    Args:
        seq: Sequence to split
        count: Number of chunks

    Returns:
        List of chunks
    """
    avg = len(seq) / float(count)
    res = []
    i = 0.0

    while i < len(seq):
        res.append(seq[int(i):int(i + avg)])
        i += avg

    return res


def compare(x, y):
    """Compares two chunk items.

    Args:
        x: First item to compare
        y: Second item to compare

    Returns:
        < 0 if x is less than y, 0 if they are equal, > 0 if x is greater
    """
    return x[0] - y[0]


def bubble_down(heap, index):
    """Moves item down to correct place in min heap.

    Args:
        heap: Heap
        index: Item index
    """
    min_index = index

    for i in xrange(index * 2 + 1, min(len(heap), index * 2 + 3)):
        if compare(heap[i], heap[min_index]) < 0:
            min_index = i

    if min_index != index:
        heap[index], heap[min_index] = heap[min_index], heap[index]
        bubble_down(heap, min_index)


def sort(lst):
    """Parallel merge sort running on multiple cores. Splits given sequence
    to even chunks which are then sorted by separate cores using sorted builtin.
    Once every core has finished chunks are merged together using min-heap.

    Since Python has GIL multiple processes needs to be used instead of threads
    which would block each other.

    Args:
        lst: List to sort

    Returns:
        List of sorted items
    """
    chunks = chunk(lst, multiprocessing.cpu_count())
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    # Build heap of [current, iterator] items
    heap = [[next(it), it] for it in
            (iter(c) for c in pool.map(sorted, chunks) if c)]
    for i in xrange((len(heap) - 1) / 2, -1, -1):
        bubble_down(heap, i)

    # Merge items from heap, note that since the number of chunks is typically
    # low merging might be faster using simple list
    res = []
    while heap:
        res.append(heap[0][0])
        try:
            heap[0][0] = next(heap[0][1])
        except StopIteration:
            if len(heap) == 1:
                break
            heap[0] = heap.pop()
        bubble_down(heap, 0)

    return res

# pylint: disable=C0103
if __name__ == '__main__':
    sample_size = 1000000
    print 'Sorting {} items'.format(sample_size)

    multiprocessing.freeze_support()
    source = [random.randint(0, sample_size / 2) for _ in xrange(sample_size)]
    start = time.clock()
    sort(source)

    print 'Parallel sort running on {} cores: {} secs'.format(
        multiprocessing.cpu_count(),
        time.clock() - start
    )

    start = time.clock()
    sorted(source)

    print 'Built-in sorted: {} secs'.format(time.clock() - start)
# pylint: enable=C0103
