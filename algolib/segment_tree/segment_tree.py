"""Maximum segment tree which can be easily customized for other purposes
(e.g. min, sum) by changing max calls appropriately. In order to improve
performance all the items are always on the lowest level of the tree
so that they can be accessed in O(1) time.

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


class SegmentTree(object):
    """Maximum segment tree.

    Attributes:
        __tree: List storing the values, children can be found from indexes
            index * 2 + 1 and index * 2 + 1
    """

    def __init__(self, seq=None, size=0):
        """Initializer, initializes segment tree from given sequence or empty
        segment tree of given size.

        Args:
            seq: Values to store in segment tree
            size: Size of segment tree in case sequence was not given
        """
        size = len(seq) if seq else size
        depth = int(ceil(log(size, 2)))

        if seq:
            lowest_lvl = 2 ** depth
            seq = list(seq)
            tree = [0] * (lowest_lvl - 1) + seq + [0] * (lowest_lvl - size)

            for i in range(depth - 1, -1, -1):
                for j in range(2 ** i - 1, 2 ** (i + 1) - 1):
                    tree[j] = max(tree[2 * j + 1], tree[2 * j + 2])
        else:
            tree = [0] * (2 ** (depth + 1) - 1)

        self.__tree = tree

    def __str__(self):
        return str(self.__tree)

    def query_point(self, index):
        """Returns value in given index.

        Args:
            index: Index of the value to return

        Returns:
            Value in given index
        """
        return self.__tree[len(self.__tree) // 2 + index]

    def query_left(self, index):
        """Returns the maximum value in range 0...index (inclusive).

        Args:
            index: Last index of the query

        Returns:
            Maximum value in the range
        """
        index += len(self.__tree) // 2

        # Find first node that is not a right child
        while index and index % 2 == 0:
            index = (index - 1) // 2

        res = self.__tree[index]

        # If node is right child check sibling
        while index:
            if index % 2 == 0:
                res = max(res, self.__tree[index - 1])
            index = (index - 1) // 2

        return res

    def query_right(self, index):
        """Returns maximum value in range index...length-1 (inclusive).

        Args:
            index: First index of the query

        Returns:
            Maximum value in the range
        """
        index += len(self.__tree) // 2

        # Find first node that is not a left child
        while index % 2:
            index = (index - 1) // 2

        res = self.__tree[index]

        # If node is left child check sibling
        while index:
            if index % 2:
                res = max(res, self.__tree[index + 1])
            index = (index - 1) // 2

        return res

    def query_range(self, r_start, r_end):
        """Returns maximum value in range r_start...r_end (inclusive).

        Args:
            r_start: First index of the query
            r_end: Last index of the query

        Returns:
            Maximum value in the range
        """
        start = len(self.__tree) // 2 + r_start
        end = len(self.__tree) // 2 + r_end

        val_s = self.__tree[start]
        val_e = self.__tree[end]

        # Traverse up the tree while there are values between start and end
        while end - start > 1:

            # If start is left child then consider right child as well
            if start % 2:
                val_s = max(val_s, self.__tree[start + 1])

            # If end is right child then consider left child as well
            if end % 2 == 0:
                val_e = max(val_e, self.__tree[end - 1])

            start = (start - 1) // 2
            end = (end - 1) // 2

        return max(val_s, val_e)

    def update_point(self, index, val):
        """Updates value in given index.

        Args:
            index: Index to update
            val: New value
        """
        index += len(self.__tree) // 2
        self.__tree[index] = val

        # Update parent nodes while the new value is larger than current
        while index:
            index = (index - 1) // 2
            if val <= self.__tree[index]:
                break
            self.__tree[index] = val

    def update_range(self, range_start, range_end, value):
        """Updates all values in range_start...range_end (inclusive).

        Args:
            range_start: Range start
            range_end: Range end
            value: New value
        """
        return self.__update_range(0, 0, len(self.__tree) // 2,
                                   range_start, range_end, value)

    # pylint: disable=too-many-arguments
    def __update_range(self, index, s_start, s_end, r_start, r_end, value):
        # Stop if out of range or update is not needed
        if r_end < s_start or r_start > s_end or self.__tree[index] == value:
            return

        # Single value segment, update self and stop
        if s_start == s_end:
            self.__tree[index] = value
            return

        # Multi value segment, update both children and then update self
        mid = s_start + (s_end - s_start) // 2
        self.__update_range(index * 2 + 1, s_start, mid,
                            r_start, r_end, value)
        self.__update_range(index * 2 + 2, mid + 1, s_end,
                            r_start, r_end, value)
        self.__tree[index] = max(self.__tree[index * 2 + 1],
                                 self.__tree[index * 2 + 2])
    # pylint: enable=too-many-arguments
