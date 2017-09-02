"""Priority queue where keys are stored to buckets in order to make
the underlying heap smaller. Implements same interface as PriorityQueue.

Time complexity of the operations where k is number of unique priorities:
- creation: O(n)
- push: O(1) if key with same priority is present, O(log k) if not
- pop: O(1) if there are multiple key with minimum priority, O(log k) if not
- change priority: O(1) if there are multiple keys with both original and new
  priority, O(log k) if not
- query min: O(1)
"""
from collections import defaultdict
import heapq


class BucketQueue(object):
    """Priority queue that stores keys with same priority in buckets instead
    of items in a heap.

    Attributes:
        __keys: {key: priority} dictionary.
        __buckets: {priority: set} dictionary where set contains keys.
        __heap: Binary heap of unique priorities.
        __position: {priority: bucket index} dictionary.
    """
    def __init__(self, it=tuple()):
        """Initializes new object, takes optional iterable as argument.

        Args:
            it: Optional iterable containing priority, key pairs.
        """
        self.__keys = {}
        self.__buckets = defaultdict(set)

        for priority, key in it:
            self.__buckets[priority].add(key)
            self.__keys[key] = priority

        self.__heap = list(self.__buckets.keys())
        heapq.heapify(self.__heap)
        self.__position = {x: i for i, x in enumerate(self.__heap)}

    def __len__(self):
        return len(self.__keys)

    def __swap(self, x, y):
        self.__position[self.__heap[x]] = y
        self.__position[self.__heap[y]] = x
        self.__heap[x], self.__heap[y] = self.__heap[y], self.__heap[x]

    def __bubble_down(self, index):
        while True:
            min_index = index
            max_len = min(len(self.__heap), index * 2 + 3)
            for i in range(index * 2 + 1, max_len):
                if self.__heap[i] < self.__heap[min_index]:
                    min_index = i

            if min_index == index:
                break

            self.__swap(index, min_index)
            index = min_index

    def __bubble_up(self, index):
        while index:
            parent = (index - 1) // 2
            if self.__heap[parent] <= self.__heap[index]:
                break
            self.__swap(parent, index)
            index = parent

    def push(self, priority, key):
        """Pushes new item to priority queue.

        Args:
            priority: Priority.
            key: Item key, must be unique and hashable.
        """
        self.__buckets[priority].add(key)
        self.__keys[key] = priority

        if len(self.__buckets[priority]) > 1:
            return

        index = len(self.__heap)
        self.__position[priority] = index
        self.__heap.append(priority)
        self.__bubble_up(index)

    def min(self):
        """Returns minimum item in the priority_queue.

        Returns:
            Minimum item as (priority, key) tuple.
        """
        return self.__heap[0], next(iter(self.__buckets[self.__heap[0]]))

    def __remove_bucket(self, priority):
        del self.__buckets[priority]
        index = self.__position.pop(priority)
        self.__swap(index, len(self.__heap) - 1)
        del self.__heap[-1]

        if index != len(self.__heap):
            if index and self.__heap[index] < self.__heap[(index - 1) // 2]:
                self.__bubble_up(index)
            else:
                self.__bubble_down(index)

    def pop(self):
        """Pops minimum item off the priority queue.

        Returns:
            Minimum item as (priority, key) tuple.
        """
        priority = self.__heap[0]
        bucket = self.__buckets[priority]
        key = bucket.pop()
        del self.__keys[key]

        if not bucket:
            self.__remove_bucket(priority)

        return priority, key

    def change_priority(self, priority, key):
        """Changes priority of a key.

        Args:
            priority: Priority.
            key: Item key.
        """
        old_priority = self.__keys[key]
        old_bucket = self.__buckets[old_priority]
        old_bucket.discard(key)
        self.push(priority, key)

        if not old_bucket:
            self.__remove_bucket(old_priority)
