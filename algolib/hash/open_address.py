"""Hash-table that uses open addressing where collisions are solved by storing
the item to next free slot.
"""

from itertools import chain, islice

# Sentinel object used to mark unused slots
SENTINEL = object()

# Default size
INITIAL_SIZE = 7

# Max load factor, once this is reached table will be grown
LOAD_FACTOR = 0.7

# Growth factor
GROW = 2


class Hash(object):
    """Hash table that uses open addressing.

    Attributes:
        table: Table storing items, uses SENTINEL to mark unused slots
        size: Number of items in the table
    """
    def __init__(self, it=None):
        """Initialized.

        Args:
            it: Optional iterable which contents are added to table.
        """
        self.table = [SENTINEL] * INITIAL_SIZE
        self.size = 0
        self.extend(it or [])

    def __str__(self):
        return 'Hash({})'.format(list(self))

    def __len__(self):
        return self.size

    def __iter__(self):
        for x in self.table:
            if x is not SENTINEL:
                yield x

    @staticmethod
    def __index_from_item(item, table):
        """Iterates over indexes in table starting from given item. First free
        index should be used to store the item.

        Args:
            item: Item to hash
            table: Table containing items

        Yields:
            Indexes where item should be stored in preference order
        """
        size = len(table)
        start = hash(item) % size
        for i in xrange(start, start + size):
            yield i % size

    @staticmethod
    def __add(table, item):
        """Adds given item to table.

        Args:
            table: Table to add the item
            item: Item to add

        Returns:
            1 if item was added, 0 if it wasn't (it was already in the table)
        """
        for i in Hash.__index_from_item(item, table):
            if table[i] is SENTINEL:
                table[i] = item
                return 1
            elif table[i] == item:
                break

        # Never reached without break
        return 0

    def add(self, item):
        """Adds item to hash table

        Args:
            item: Item to add
        """
        if self.size == int(len(self.table) * LOAD_FACTOR):
            # Rehash whole table
            table = [SENTINEL] * (GROW * len(self.table))
            for x in self.table:
                if x is not SENTINEL:
                    Hash.__add(table, x)

            self.table = table

        self.size += Hash.__add(self.table, item)

    def extend(self, it):
        """Adds items from given iterable to hash table.

        Args:
            it: Itertable containing items
        """
        for x in it:
            self.add(x)

    def __find(self, item):
        """Searches index of an item in the hash table.

        Args:
            item: Item to search

        Returns:
            Index where the item is stored, -1 if not found
        """
        for i in Hash.__index_from_item(item, self.table):
            x = self.table[i]
            if x is SENTINEL:
                break
            elif x == item:
                return i

        # Never reached without break
        return -1

    def __contains__(self, item):
        return self.__find(item) != -1

    def isdisjoint(self, other):
        """Check if two hashtables are disjoint (=don't contain the same item).

        Args:
            other: Other hash table

        Returns:
            True if hashtables are disjoint, False if not
        """
        small, big = sorted((self, other), key=len)
        return all(x not in big for x in small)

    def __le__(self, other):
        return len(self) <= len(other) and all(x in other for x in self)

    def __lt__(self, other):
        return len(self) < len(other) and all(x in other for x in self)

    def __eq__(self, other):
        return len(self) == len(other) and all(x in other for x in self)

    def __ge__(self, other):
        return len(self) >= len(other) and all(x in self for x in other)

    def __gt__(self, other):
        return len(self) > len(other) and all(x in self for x in other)

    def __ne__(self, other):
        return len(self) != len(other) or any(x not in other for x in self)

    def __and__(self, other):
        small, big = sorted((self, other), key=len)
        return Hash(x for x in small if x in big)

    def __or__(self, other):
        return Hash(chain(self, other))

    def __sub__(self, other):
        return Hash(x for x in self if x not in other)

    def __xor__(self, other):
        res = Hash(x for x in self if x not in other)
        res.extend(x for x in other if x not in self)

        return res

    def clear(self):
        """Removes all items from the hashtable."""
        self.table = [SENTINEL] * INITIAL_SIZE
        self.size = 0

    def __remove(self, index):
        """Removes item from hashtable.

        Args:
            index: Index of the item
        """
        # In open addressing scheme all the items immediately following the
        # removed item need to be hashed. Collect all them to rehash.
        rehash = []
        length = len(self.table)
        for i in xrange(index, index + length):
            i %= len(self.table)
            if self.table[i] == SENTINEL:
                break
            rehash.append(self.table[i])
            self.table[i] = SENTINEL
            self.size -= 1

        # Insert back all except the one that needed to be removed
        self.extend(islice(rehash, 1, None))

    def pop(self):
        """Removes random item from hashtable and returns it.

        Returns:
            Removed item

        Raises:
            KeyError in case hashtable is empty
        """
        # If items would be stored to doubly linked list time complexity
        # would be O(1)
        for i in xrange(len(self.table)):
            x = self.table[i]
            if x != SENTINEL:
                self.__remove(i)
                return x

        raise KeyError

    def discard(self, item):
        """Removes given item from hash,

        Args:
            item: Item to remove
        """
        index = self.__find(item)
        if index != -1:
            self.__remove(index)

    def remove(self, item):
        """Removes given item from hash.

        Args:
            item: Item to remove

        Raises:
            KeyError if item is not present
        """
        index = self.__find(item)
        if index == -1:
            raise KeyError

        self.__remove(index)

    def __ior__(self, other):
        for x in other:
            self.add(x)

        return self

    def __iand__(self, other):
        for i, x in enumerate(self.table):
            if x not in other:
                self.table[i] = SENTINEL
                self.size -= 1

        return self

    def __isub__(self, other):
        for x in other:
            self.discard(x)

        return self

    def __ixor__(self, other):
        self.__isub__(self & other)
        return self
