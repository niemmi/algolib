"""Disjoint-set data structure that allows efficient way of finding which set
item belongs to and merging two different sets.

Time complexity of the operations:
- Find which set item belongs to: O(log n)
- Merging two sets: O(log n)
- Checking if two items belong to same set: O(log n)

For more information see Wikipedia:
https://en.wikipedia.org/wiki/Disjoint-set_data_structure
"""


class DisjointSet(object):
    """Disjoint-set data structure that allows user to check which set item
    belongs to and merging two different sets.

    Attributes:
        _items: Dictionary of items belonging to set where keys are items
            and values are pairs [parent, number of items in set]
    """
    def __init__(self, it):
        """Initializer, initializes Disjoint-set with items from given iterable.

        Args:
            it: Iterable of items to add to the object.
        """
        self._items = {item: [item, 1] for item in it}

    def __len__(self):
        return len(self._items)

    def find(self, item):
        """Returns the set where this item belongs to. If items x & y belong
        to the same set then find(x) == find(y).

        Args:
            item: Item whose set to search.

        Returns:
            Set identifier which is one of the items in the object.
        """
        while True:
            parent = self._items[item][0]
            if parent == item:
                # Note that we could do add path compression here to make
                # subsequent searches faster
                return item
            item = parent

    def union(self, x, y):
        """Merges sets containing two different items together. If items already
        belong to same set does nothing.

        Args:
            x: First item.
            y: Second item.
        """
        parent_x = self.find(x)
        parent_y = self.find(y)

        if parent_x != parent_y:
            merge_from, merge_to = sorted([parent_x, parent_y],
                                          key=lambda x: self._items[x][1])
            self._items[merge_from][0] = merge_to
            self._items[merge_to][1] += self._items[merge_from][1]

    def same_component(self, x, y):
        """Returns boolean value telling if two different items belong to
        same set.

        Args:
            x: First item.
            y: Second item.

        Returns:
            True if items belong to same set, False if not.
        """
        return self.find(x) == self.find(y)
