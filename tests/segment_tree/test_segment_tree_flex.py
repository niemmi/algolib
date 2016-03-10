import sys
import unittest

from .context import segment_tree_flex
from operator import add


class TestSegmentTree(unittest.TestCase):
    def test_sum(self):
        nums = range(1, 6)
        tree = segment_tree_flex.SegmentTree(nums)
        self.assertEqual(sum(nums), tree.query_range(0, 4))
        self.assertEqual(sum(nums[0:2]), tree.query_range(0, 1))
        self.assertEqual(nums[4], tree.query_range(4, 4))
        self.assertEqual(nums[2], tree.query_range(2, 2))

    def test_min(self):
        nums = range(1, 6)
        tree = segment_tree_flex.SegmentTree(nums, min, sys.maxint)
        self.assertEqual(min(nums), tree.query_range(0, 4))
        self.assertEqual(min(nums[0:2]), tree.query_range(0, 1))
        self.assertEqual(nums[4], tree.query_range(4, 4))
        self.assertEqual(nums[2], tree.query_range(2, 2))

    def test_max(self):
        nums = range(1, 6)
        tree = segment_tree_flex.SegmentTree(nums, max, None)
        self.assertEqual(max(nums), tree.query_range(0, 4))
        self.assertEqual(max(nums[0:2]), tree.query_range(0, 1))
        self.assertEqual(nums[4], tree.query_range(4, 4))
        self.assertEqual(nums[2], tree.query_range(2, 2))

    def test_update(self):
        nums = range(1, 6)
        tree = segment_tree_flex.SegmentTree(nums, add, 0)
        tree.update_point(2, 0)
        nums[2] = 0
        self.assertEqual(sum(nums), tree.query_range(0, 4))
        self.assertEqual(sum(nums[0:2]), tree.query_range(0, 1))
        self.assertEqual(nums[4], tree.query_range(4, 4))
        self.assertEqual(nums[2], tree.query_range(2, 2))

    def test_get_each(self):
        nums = [1, 3, 6]
        tree = segment_tree_flex.SegmentTree(nums, add, 0)
        for i in xrange(3):
            self.assertEqual(nums[i], tree.query_range(i, i))

    def test_update_each(self):
        nums = range(1, 11)
        for i in xrange(1, len(nums) + 1):
            src = nums[:i]
            tree = segment_tree_flex.SegmentTree(src, add, 0)

            for j in xrange(i):
                src[j] = 0
                tree.update_point(j, 0)
                self.assertEqual(sum(src), tree.query_range(0, i - 1))

if __name__ == '__main__':
    unittest.main()
