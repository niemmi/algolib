"""Priority queue that keys and returns them in priority order. Offers same
kind of  interface as heapq with added change_priority method. Elements are
stored as priority, key pairs in a list representation of heap with added dict
mapping keys to list indexes. Note that keys must be unique and hashable.

Time complexity of the operations:
- creation: O(n)
- push: O(log n)
- pop: O(log n)
- change priority value: O(log n)
- query min: O(1)
"""
from heapq import heapify


class PriorityQueue(object):
    """Priority that stores priority, key pairs and supports all common
    priority queue operations

    Attributes:
        __position: Key: index mapping of items.
        __heap: [priority, key] pairs in heapified list.
    """
    def __init__(self, it=tuple()):
        """Initializes new object, takes optional iterable as argument.

        Args:
            it: Optional iterable containing priority, key pairs.
        """
        self.__heap = [list(x) for x in it]
        heapify(self.__heap)
        self.__position = {key: i for i, (_, key) in enumerate(self.__heap)}

    def __len__(self):
        return len(self.__heap)

    def __swap(self, x, y):
        self.__position[self.__heap[x][1]] = y
        self.__position[self.__heap[y][1]] = x
        self.__heap[x], self.__heap[y] = self.__heap[y], self.__heap[x]

    def __bubble_down(self, index):
        while True:
            min_index = index
            for i in range(index * 2 + 1, min(len(self), index * 2 + 3)):
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
        index = len(self.__heap)
        self.__position[key] = index
        self.__heap.append([priority, key])
        self.__bubble_up(index)

    def min(self):
        """Returns minimum item in the priority queue.

        Returns:
            Minimum item as (priority, key) tuple.
        """
        return tuple(self.__heap[0])

    def pop(self):
        """Pops minimum item off the priority queue.

        Returns:
            Minimum item as (priority, key) tuple.
        """
        priority, key = self.__heap[0]
        self.__swap(0, len(self.__heap) - 1)
        del self.__position[key]
        del self.__heap[-1]

        if self:
            self.__bubble_down(0)

        return priority, key

    def push_pop(self, priority, key):
        """Same as push() followed by pop(), just more efficient.

        Args:
            priority: Priority.
            key: Item key, must be unique and hashable.

        Returns:
            Minimum item as (priority, key) tuple.
        """
        if not self or priority <= self.__heap[0][0]:
            return priority, key

        result_priority, result_key = self.__heap[0]
        del self.__position[result_key]

        self.__heap[0] = [priority, key]
        self.__position[key] = 0
        self.__bubble_down(0)

        return result_priority, result_key

    def replace(self, priority, key):
        """Same as pop() followed by push(), just more efficient.

        Args:
            priority: Priority.
            key: Item key, must be unique and hashable.

        Returns:
            Minimum item as (priority, key) tuple.
        """
        result_priority, result_key = self.__heap[0]
        del self.__position[result_key]

        self.__heap[0] = [priority, key]
        self.__position[key] = 0
        self.__bubble_down(0)

        return result_priority, result_key

    def change_priority(self, priority, key):
        """Changes priority of a key.

        Args:
            priority: Priority.
            key: Item key.
        """
        index = self.__position[key]
        current = self.__heap[index][0]
        self.__heap[index][0] = priority

        if priority > current:
            self.__bubble_down(index)
        else:
            self.__bubble_up(index)
