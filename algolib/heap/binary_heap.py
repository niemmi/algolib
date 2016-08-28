"""Binary heap that offers same kind of interface as heapq with added
change_value method. Elements are stored as key value pairs in a list
representation of heap with added dict mapping keys to list indexes. Note that
keys must be unique and hashable.

Time complexity of the operations:
- creation: O(n)
- push: O(log n)
- pop: O(log n)
- change priority value: O(log n)
- query min: O(1)
"""


class BinaryHeap(object):
    """Binary heap that stores key, priority pairs and supports all common heap
    operations with added possibility of changing priority value in O(log n)
    time.

    Attributes:
        __position: Key: index mapping of items.
        __heap: [key, value] pairs in heapified list.
    """
    def __init__(self, it=tuple()):
        """Initializes new object, takes optional iterable as argument.

        Args:
            it: Optional iterable containing key, priority value pairs.
        """
        self.__position = {}
        self.__heap = []

        for i, (key, value) in enumerate(it):
            self.__position[key] = i
            self.__heap.append([key, value])

        for i in xrange(len(self.__heap) / 2, -1, -1):
            self.__bubble_down(i)

    def __len__(self):
        return len(self.__heap)

    def __swap(self, x, y):
        self.__position[self.__heap[x][0]] = y
        self.__position[self.__heap[y][0]] = x
        self.__heap[x], self.__heap[y] = self.__heap[y], self.__heap[x]

    def __bubble_down(self, index):
        while True:
            min_index = index
            for i in xrange(index * 2 + 1, min(len(self), index * 2 + 3)):
                if self.__heap[i][1] < self.__heap[min_index][1]:
                    min_index = i

            if min_index == index:
                break

            self.__swap(index, min_index)
            index = min_index

    def __bubble_up(self, index):
        while index:
            parent = (index - 1) / 2
            if self.__heap[parent][1] <= self.__heap[index][1]:
                break
            self.__swap(parent, index)
            index = parent

    def push(self, key, value):
        """Pushes new item to heap.

        Args:
            key: Item key, must be unique and hashable.
            value: Priority value.
        """
        index = len(self.__heap)
        self.__position[key] = index
        self.__heap.append([value, key])
        self.__bubble_up(index)

    def min(self):
        """Returns minimum item in the heap.

        Returns:
            Minimum item as (key, value) tuple.
        """
        return tuple(self.__heap[0])

    def pop(self):
        """Pops minimum item off the heap.

        Returns:
            Minimum item as (key, value) tuple.
        """
        key, value = self.__heap[0]
        self.__swap(0, len(self.__heap) - 1)
        del self.__position[key]
        del self.__heap[-1]

        if self:
            self.__bubble_down(0)

        return key, value

    def push_pop(self, key, value):
        """Same as heap.push() followed by heap.pop(), just more efficient.

        Args:
            key: Item key, must be unique and hashable.
            value: Priority value.

        Returns:
            Minimum item as (key, value) tuple.
        """
        if self and value <= self.__heap[0][1]:
            return key, value

        result_key, result_value = self.__heap[0]
        del self.__position[result_key]

        self.__heap[0] = [value, key]
        self.__position[key] = 0
        self.__bubble_down(0)

        return result_key, result_value

    def replace(self, key, value):
        """Same as heap.pop() followed by heap.push(), just more efficient.

        Args:
            key: Item key, must be unique and hashable.
            value: Priority value.

        Returns:
            Minimum item as (key, value) tuple.
        """
        result_key, result_value = self.__heap[0]
        del self.__position[result_key]

        self.__heap[0] = [key, value]
        self.__position[key] = 0
        self.__bubble_down(0)

        return result_key, result_value

    def change_value(self, key, value):
        """Changes priority value of an item.

        Args:
            key: Item key.
            value: Priority value.
        """
        index = self.__position[key]
        current = self.__heap[index][1]
        self.__heap[index][1] = value

        if value > current:
            self.__bubble_down(index)
        else:
            self.__bubble_up(index)
