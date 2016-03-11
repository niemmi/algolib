"""Multipurpose segment tree that can be customized without code changes by
merge function given as a parameter. By default contains the sum for a range.
Note that this implementation is bit slower than dedicated one because of
added indirection and couple optimizations that are doable only if merge
function is known.

Time complexity of the operations:
- creation: O(n)
- point query: O(1)
- range query: O(log n)
- point update: O(log n)
- range update: O(k) where k equals the length of updated range

For more information about segment trees see:
- https://en.wikipedia.org/wiki/Segment_tree
- http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/
"""
from math import ceil, log
from operator import add


class SegmentTree(object):
    """Maximum segment tree"""

    def __init__(self, seq=None, merge=add, size=0, default=0):
        """Constructor, creates segment tree from given sequence or empty
        segment tree of given size.

        Args:
            seq: Items to store in segment tree
            merge: Merge function that returns combined value for two children
            size: Size of segment tree in case sequence was not given
            default: Default value, used in case that size has been given
                instead of sequence
        """
        size = len(seq) if seq else size
        depth = int(ceil(log(size, 2)))

        if seq:
            lowest_lvl = 2 ** depth
            tree = [0] * (lowest_lvl - 1) + seq + [0] * (lowest_lvl - size)

            for i in xrange(depth - 1, -1, -1):
                for j in range(2 ** i - 1, 2 ** (i + 1) - 1):
                    tree[j] = merge(tree[2 * j + 1], tree[2 * j + 2])
        else:
            tree = [default] * (2 ** (depth + 1) - 1)

        self.__tree = tree
        self.__merge = merge

    def __str__(self):
        return str(self.__tree)

    def query_point(self, index):
        """Returns item in given index."""
        return self.__tree[len(self.__tree) / 2 + index]

    def query_left(self, index):
        """Returns the maximum item in range 0...index (inclusive).

        Args:
            index: Last index of the query

        Returns:
            Maximum item in the range
        """
        index += len(self.__tree) / 2

        # Find first node that is not a right child
        while index and index % 2 == 0:
            index = (index - 1) / 2

        res = self.__tree[index]

        # If node is right child check sibling
        while index:
            if index % 2 == 0:
                res = self.__merge(res, self.__tree[index - 1])
            index = (index - 1) / 2

        return res

    def query_right(self, index):
        """Returns maximum item in range index...length-1 (inclusive).

        Args:
            index: First index of the query

        Returns:
            Maximum item in the range
        """
        index += len(self.__tree) / 2

        # Find first node that is not a left child
        while index % 2:
            index = (index - 1) / 2

        res = self.__tree[index]

        # If node is left child check sibling
        while index:
            if index % 2:
                res = self.__merge(res, self.__tree[index + 1])
            index = (index - 1) / 2

        return res

    def query_range(self, r_start, r_end):
        """Returns maximum item in r_start...r_end (inclusive).

        Args:
            r_start: First index of the query
            r_end: Last index of the query

        Returns:
            Maximum item in the range
        """
        if r_start == r_end:
            return self.query_point(r_start)

        start = len(self.__tree) / 2 + r_start
        end = len(self.__tree) / 2 + r_end

        val_s = self.__tree[start]
        val_e = self.__tree[end]

        # Loop while end & start are not siblings
        while end - start > 1:

            # If start is left child then consider right child as well
            if start % 2:
                val_s = self.__merge(val_s, self.__tree[start + 1])

            # If end is right child then consider left child as well
            if end % 2 == 0:
                val_e = self.__merge(val_e, self.__tree[end - 1])

            start = (start - 1) / 2
            end = (end - 1) / 2

        return self.__merge(val_s, val_e)

    def update_point(self, index, val):
        """Updates item in given index.

        Args:
            index: Index to update
            val: New value
        """
        index += len(self.__tree) / 2
        self.__tree[index] = val

        # Update parent nodes while the new value is larger than current
        while index:
            index = (index - 1) / 2
            new_val = self.__merge(self.__tree[index * 2 + 1],
                                   self.__tree[index * 2 + 2])
            if new_val == self.__tree[index]:
                break
            self.__tree[index] = new_val

    def update_range(self, range_start, range_end, value):
        """Updates all items in range_start...range_end (inclusive).

        Args:
            range_start: Range start
            range_end: Range end
            value: New value
        """
        return self.__update_range(0, 0, len(self.__tree) / 2,
                                   range_start, range_end, value)

    # pylint: disable=too-many-arguments
    def __update_range(self, index, s_start, s_end, r_start, r_end, value):
        # Stop if out of range
        if r_end < s_start or r_start > s_end:
            return

        # Single item segment, update value and stop
        if s_start == s_end:
            self.__tree[index] = value
            return

        # Multi item segment, update both children and then update self
        mid = s_start + (s_end - s_start) / 2
        self.__update_range(index * 2 + 1, s_start, mid,
                            r_start, r_end, value)
        self.__update_range(index * 2 + 2, mid + 1, s_end,
                            r_start, r_end, value)
        self.__tree[index] = self.__merge(self.__tree[index * 2 + 1],
                                          self.__tree[index * 2 + 2])
    # pylint: enable=too-many-arguments
