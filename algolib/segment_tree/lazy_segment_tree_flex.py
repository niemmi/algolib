"""Simple and flexible implementation of segment tree with lazy propagation.
Tree supports range query and range update with user given merge and update
functions. Default mode is range sum with add function. Can be customized for
other purposes (e.g. min, max) or operations (subtraction, div, multiply) by
giving appropriate functions to constructor.

Time complexity of the operations:
- creation: O(n)
- range query: O(log n)
- range update: O(log n)

For more information about segment trees with lazy propagation see:
- http://www.geeksforgeeks.org/lazy-propagation-in-segment-tree/
"""
from math import ceil, log
from operator import add


def update_sum(value, diff, count):
    """Given the original value, difference and number values in the segment
    return new segment value.

    Args:
        value: Old value
        diff: Difference
        count: Number of values in segment

    Returns:
        Updated sum of all values in the segment
    """
    return value + diff * count


class SegmentTree(object):
    """Maximum segment tree with lazy propagation of add operator.

    Attributes:
        __tree: List storing the values, children can be found from indexes
            index * 2 + 1 and index * 2 + 1
        __pending: Pending updates, if value of child is being read pending
            update needs to be added to it in order to get correct value
        __merge_value: Merges two values to one
        __update: Applies pending update to value, first argument is value,
            second is update and third is number values being updated
        __merge_update: Merges two pending updates to one, first param is
            current pending update and second is diff given to update function
    """
    # pylint: disable=too-many-arguments
    def __init__(self, seq=None, merge_value=add, update=update_sum,
                 merge_update=add, default_value=0, default_update=0, size=0):
        """Creates new instance of the segment tree.

        Args:
            seq: Sequence of values to add, if not passed then size and
                default_value is used to initialize the tree
            merge_value: Function to merge two value, takes in two values
                and returns merged value (e.g. for min segment tree min could
                be used)
            update: Function to update a segment, takes in three args:
                old value, difference coming from caller and number of values
                in segment. Should return the updated value for the segment.
            merge_update: Function to merge two pending updates together,
                first arg is current update value and second one difference
                coming from caller
            default_value: Default value to be used to initialize tree in case
                that seq is not given
            default_update: Default update value to initialize pending updates
            size: Size of the tree, used in case that seq wasn't provided
        """
        if seq:
            size = len(seq) if seq else size
        else:
            seq = [default_value] * size

        depth = int(ceil(log(size, 2)))
        tree_size = 2 ** (depth + 1) - 1

        self.__size = size
        self.__tree = [0] * tree_size
        self.__pending = [default_update] * (2 ** depth - 1)
        self.__merge_value = merge_value
        self.__update = update
        self.__merge_update = merge_update
        self.__make_segment(seq, 0, size - 1, 0)
    # pylint: enable=too-many-arguments

    def __make_segment(self, seq, s_start, s_end, index):
        if s_start == s_end:
            self.__tree[index] = seq[s_start]
        else:
            mid = s_start + (s_end - s_start) / 2
            self.__make_segment(seq, s_start, mid, index * 2 + 1)
            self.__make_segment(seq, mid + 1, s_end, index * 2 + 2)
            self.__tree[index] = self.__merge_value(self.__tree[index * 2 + 1],
                                                    self.__tree[index * 2 + 2])

    def __str__(self):
        return str(self.__tree) + ',' + str(self.__pending)

    def query_range(self, r_start, r_end):
        """Returns merged value in range r_start...r_end (inclusive).

        Args:
            r_start: First index of the query
            r_end: Last index of the query

        Returns:
            Maximum value in the range
        """
        return self.__query(0, 0, self.__size - 1, r_start, r_end)

    # pylint: disable=too-many-arguments
    def __query(self, index, s_start, s_end, r_start, r_end):
        # If range fully covers this segment
        if r_start <= s_start and r_end >= s_end:
            return self.__tree[index]

        mid = s_start + (s_end - s_start) / 2

        # If range only intersects with left child
        if mid >= r_end:
            res = self.__query(index * 2 + 1, s_start, mid,
                               r_start, r_end)
        # If range only intersects with right child
        elif mid < r_start:
            res = self.__query(index * 2 + 2, mid + 1, s_end,
                               r_start, r_end)
        # If range intersects both children
        else:
            left = self.__query(index * 2 + 1, s_start, mid, r_start, r_end)
            right = self.__query(index * 2 + 2, mid + 1, s_end, r_start, r_end)
            res = self.__merge_value(left, right)

        # Update the value returned from children
        count = min(s_end, r_end) - max(s_start, r_start) + 1
        return self.__update(res, self.__pending[index], count)
    # pylint: enable=too-many-arguments

    def update_range(self, r_start, r_end, diff):
        """Updates all values in range_start...range_end (inclusive).

        Args:
            r_start: Range start
            r_end: Range end
            diff: Update value
        """
        self.__update_range(0, 0, self.__size - 1, r_start, r_end, diff)

    # pylint: disable=too-many-arguments
    def __update_range(self, index, s_start, s_end, r_start, r_end, diff):
        count = s_end - s_start + 1

        # Range covers every value in segment, we can stop here
        if s_start >= r_start and s_end <= r_end:
            self.__tree[index] = self.__update(self.__tree[index], diff, count)
            if s_start != s_end:
                self.__pending[index] = self.__merge_update(
                    self.__pending[index], diff)
            return

        mid = s_start + (s_end - s_start) / 2
        # Only values in left child need to be updated
        if mid >= r_end:
            self.__update_range(index * 2 + 1, s_start, mid, r_start,
                                r_end, diff)
        # Only values in right child need to be updated
        elif mid < r_start:
            self.__update_range(index * 2 + 2, mid + 1, s_end, r_start,
                                r_end, diff)
        # Both children need to be updated
        else:
            self.__update_range(index * 2 + 1, s_start, mid, r_start,
                                r_end, diff)
            self.__update_range(index * 2 + 2, mid + 1, s_end, r_start,
                                r_end, diff)

        # Query values from children, merge & update them and set node value
        val = self.__merge_value(self.__tree[index * 2 + 1],
                                 self.__tree[index * 2 + 2])
        self.__tree[index] = self.__update(val, self.__pending[index], count)
    # pylint: enable=too-many-arguments
