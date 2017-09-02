import unittest
from .context import lazy_segment_tree


class TestSegmentTree(unittest.TestCase):
    def test_query_point(self):
        nums = range(1, 6)
        tree = lazy_segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            self.assertEqual(nums[i], tree.query_point(i))

    def test_query_left(self):
        nums = range(6)
        tree = lazy_segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            self.assertEqual(max(nums[:i+1]), tree.query_left(i))

    def test_query_right(self):
        nums = list(range(1, 6)) + list(range(5, 0, -1))
        tree = lazy_segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            self.assertEqual(max(nums[i:]), tree.query_right(i))

    def test_query_range(self):
        nums = list(range(1, 6)) + list(range(5, 0, -1))
        tree = lazy_segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            for j in range(i, len(nums)):
                self.assertEqual(max(nums[i:j + 1]), tree.query_range(i, j))

    def test_update_point(self):
        nums = range(1, 6)
        tree = lazy_segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            tree.update_point(i, 5)
            self.assertEqual(nums[i] + 5, tree.query_left(4))

    def test_update_left(self):
        nums = range(1, 6)
        tree = lazy_segment_tree.SegmentTree(nums)
        tree.update_left(len(nums) - 1, 1)

        for i in range(len(nums)):
            self.assertEqual(nums[i] + 1, tree.query_point(i))

    def test_update_query_left(self):
        nums = [1] * 5
        tree = lazy_segment_tree.SegmentTree(nums)
        for i in range(len(nums)):
            tree.update_left(i, 1)
            for j in range(i + 1):
                nums[j] += 1
            for j in range(len(nums)):
                self.assertEqual(max(nums[:j + 1]), tree.query_left(j))

    def test_update_query_right(self):
        nums = [1] * 5
        tree = lazy_segment_tree.SegmentTree(nums)
        for i in range(len(nums)):
            tree.update_right(i, 1)
            for j in range(i, 5):
                nums[j] += 1
            for j in range(len(nums)):
                self.assertEqual(max(nums[j:]), tree.query_right(j))

    def test_update_query_range(self):
        nums = [1] * 5
        tree = lazy_segment_tree.SegmentTree(nums)
        for i in range(len(nums)):
            tree.update_right(i, 1)
            for j in range(i, 5):
                nums[j] += 1
            for j in range(len(nums)):
                for k in range(j, len(nums)):
                    self.assertEqual(max(nums[j:k + 1]), tree.query_range(j, k))

    def test_update_range(self):
        nums = list(range(5))
        tree = lazy_segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                tree.update_range(i, j - 1, 1)
                for k in range(i, j):
                    nums[k] += 1
                    self.assertEqual(nums[k], tree.query_point(k))
