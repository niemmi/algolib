import unittest
from .context import lazy_segment_tree_flex
from operator import mul


def update_min_max(value, diff, _count):
    return value + diff


class TestSegmentTree(unittest.TestCase):
    def test_sum(self):
        nums = [1, 2, 3, 4, 5]
        tree = lazy_segment_tree_flex.SegmentTree(nums)
        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                self.assertEqual(sum(nums[i:j]), tree.query_range(i, j - 1))

    def test_max(self):
        nums = [2, 5, 1, 4, 3]
        tree = lazy_segment_tree_flex.SegmentTree(nums, max, update_min_max)
        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                self.assertEqual(max(nums[i:j]), tree.query_range(i, j - 1))

    def test_update_max(self):
        nums = list(range(5))
        tree = lazy_segment_tree_flex.SegmentTree(nums, max, update_min_max)

        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                for k in range(i, j):
                    nums[k] += 1
                tree.update_range(i, j - 1, 1)
                self.assertEqual(max(nums), tree.query_range(0, len(nums) - 1))

        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                self.assertEqual(max(nums[i:j]), tree.query_range(i, j - 1))

    def test_update_sum(self):
        nums = list(range(5))
        tree = lazy_segment_tree_flex.SegmentTree(nums)

        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                for k in range(i, j):
                    nums[k] += 1
                tree.update_range(i, j - 1, 1)
                self.assertEqual(sum(nums), tree.query_range(0, len(nums) - 1))

        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                self.assertEqual(sum(nums[i:j]), tree.query_range(i, j - 1))

    def test_update_sum_mul(self):
        def update_mul(value, diff, _count):
            return value * diff
        nums = [1] * 5
        tree = lazy_segment_tree_flex.SegmentTree(size=5, default_value=1,
                                                  default_update=1,
                                                  update=update_mul,
                                                  merge_update=mul
                                                  )

        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                for k in range(i, j):
                    nums[k] *= 2
                tree.update_range(i, j - 1, 2)
                self.assertEqual(sum(nums), tree.query_range(0, len(nums) - 1))

        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                self.assertEqual(sum(nums[i:j]), tree.query_range(i, j - 1))
