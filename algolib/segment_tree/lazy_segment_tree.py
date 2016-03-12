"""Non-recursive implementation of segment tree with lazy propagation. Tree
supports maximum range query and range update with add operator. Can be
customized for other purposes (e.g. min, sum) or operations
(subtraction, div, multiply).

In order to improve performance all the items are always on the lowest level.
All non-leaf elements will also store pending updates that will be applied when
child value is being read.

Time complexity of the operations:
- creation: O(n)
- point query: O(log n)
- range query: O(log n)
- point update: O(log n)
- range update: O(log n)

For more information about segment trees with lazy propagation see:
- http://www.geeksforgeeks.org/lazy-propagation-in-segment-tree/
"""
from math import ceil, log


class SegmentTree(object):
    """Maximum segment tree with lazy propagation of add operator.

    Attributes:
        __tree: List storing the values, children can be found from indexes
            index * 2 + 1 and index * 2 + 1
        __pending: Pending updates, if value of child is being read pending
            update needs to be added to it in order to get correct value
    """

    def __init__(self, seq=None, size=0):
        """Constructor, creates segment tree from given sequence or empty
        segment tree of given size.

        Args:
            seq: Values to store in segment tree
            size: Size of segment tree in case sequence was not given
        """
        size = len(seq) if seq else size
        depth = int(ceil(log(size, 2)))

        if seq:
            lowest_lvl = 2 ** depth
            tree = [0] * (lowest_lvl - 1) + seq + [0] * (lowest_lvl - size)

            for i in xrange(depth - 1, -1, -1):
                for j in range(2 ** i - 1, 2 ** (i + 1) - 1):
                    tree[j] = max(tree[2 * j + 1], tree[2 * j + 2])
        else:
            tree = [0] * (2 ** (depth + 1) - 1)

        self.__tree = tree
        self.__pending = [0] * (2 ** depth - 1)

    def __str__(self):
        return str(self.__tree) + ',' + str(self.__pending)

    def query_point(self, index):
        """Returns value in given index.

        Args:
            index: Index of the value to return

        Returns:
            Value in given index
        """
        index += len(self.__tree) / 2
        res = self.__tree[index]

        # Iterate to root while adding pending updates
        while index:
            index = (index - 1) / 2
            res += self.__pending[index]

        return res

    def query_left(self, index):
        """Returns the maximum value in range 0...index (inclusive).

        Args:
            index: Last index of the query

        Returns:
            Maximum value in the range
        """
        index += len(self.__tree) / 2

        # Find first node that is not a right child
        while index and index % 2 == 0:
            index = (index - 1) / 2

        res = self.__tree[index]

        # Add pending updates to the result, if node is right child check
        # left as well
        while index:
            if index % 2 == 0:
                res = max(res, self.__tree[index - 1])
            index = (index - 1) / 2
            res += self.__pending[index]

        return res

    def query_right(self, index):
        """Returns maximum value in range index...length-1 (inclusive).

        Args:
            index: First index of the query

        Returns:
            Maximum value in the range
        """
        index += len(self.__tree) / 2

        # Find first node that is not a left child
        while index % 2:
            index = (index - 1) / 2

        res = self.__tree[index]

        # Add pending updates to the result, if node is left child check
        # left as well
        while index:
            if index % 2:
                res = max(res, self.__tree[index + 1])
            index = (index - 1) / 2
            res += self.__pending[index]

        return res

    def query_range(self, r_start, r_end):
        """Returns maximum value in range r_start...r_end (inclusive).

        Args:
            r_start: First index of the query
            r_end: Last index of the query

        Returns:
            Maximum value in the range
        """
        start = len(self.__tree) / 2 + r_start
        end = len(self.__tree) / 2 + r_end

        val_s = self.__tree[start]
        val_e = self.__tree[end]

        # Traverse up the tree while start and end are not siblings
        while (end - 1) / 2 != (start - 1) / 2:

            # If start is left child then consider right child as well
            if start % 2:
                val_s = max(val_s, self.__tree[start + 1])

            # If end is right child then consider left child as well
            if end % 2 == 0:
                val_e = max(val_e, self.__tree[end - 1])

            start = (start - 1) / 2
            end = (end - 1) / 2

            val_s += self.__pending[start]
            val_e += self.__pending[end]

        val = max(val_s, val_e)

        # Traverse to root and and pending updates
        while start:
            start = (start - 1) / 2
            val += self.__pending[start]

        return val

    def update_point(self, index, diff):
        """Adds number to given index.

        Args:
            index: Index to update
            diff: Value to add
        """
        index += len(self.__tree) / 2
        val = self.__tree[index] + diff
        self.__tree[index] = val

        # Update parent nodes if needed
        while index:
            index = (index - 1) / 2
            val += self.__pending[index]
            if val <= self.__tree[index]:
                break
            self.__tree[index] = val

    def update_left(self, index, diff):
        """Adds value to all values in range 0...index (inclusive).

        Args:
            index: Last index to update
            diff: Value to add
        """
        index += len(self.__tree) / 2

        # Handle sequence of right children and first left child
        if index and index % 2 == 0:
            while index and index % 2 == 0:
                index = (index - 1) / 2
            self.__pending[index] += diff

        self.__tree[index] += diff

        # Here index points to either root or left child and
        # current node is updated
        # Update tree values all the way to the top
        while index:
            # If this is a right child then update the left child
            if index % 2 == 0:
                self.__pending[index - 1] += diff
                self.__tree[index - 1] += diff

            # Moved up the tree
            index = (index - 1) / 2

            # Update this node
            val = max(self.__tree[index * 2 + 1], self.__tree[index * 2 + 2])
            self.__tree[index] = val + self.__pending[index]

    def update_right(self, index, diff):
        """Adds value to all values in range index...length-1 (inclusive).

        Args:
            index: First index to update
            diff: Value to add
        """
        index += len(self.__tree) / 2

        # Handle sequence of left children and first right child
        if index % 2:
            while index % 2:
                index = (index - 1) / 2
            self.__pending[index] += diff

        self.__tree[index] += diff

        # Here index points to either root or right child and
        # current node is updated
        # Update tree values all the way to the top
        while index:
            # If this is a left child then update the right child
            if index % 2:
                self.__pending[index + 1] += diff
                self.__tree[index + 1] += diff

            # Moved up the tree
            index = (index - 1) / 2

            # Update this node
            val = max(self.__tree[index * 2 + 1], self.__tree[index * 2 + 2])
            self.__tree[index] = val + self.__pending[index]
