import unittest
from .context import segment_tree


class TestSegmentTree(unittest.TestCase):
    def test_create(self):
        nums = range(1, 6)
        tree = segment_tree.SegmentTree(nums)
        for i in range(len(nums)):
            self.assertEqual(nums[i], tree.query_point(i))

    def test_query_left(self):
        nums = list(range(1, 6)) + list(range(5, 0, -1))
        tree = segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            self.assertEqual(max(nums[:i + 1]), tree.query_left(i))

    def test_query_right(self):
        nums = list(range(1, 6)) + list(range(5, 0, -1))
        tree = segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            self.assertEqual(max(nums[i:]), tree.query_right(i))

    def test_query_range(self):
        nums = list(range(1, 6)) + list(range(5, 0, -1))
        tree = segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            for j in range(i, len(nums)):
                self.assertEqual(max(nums[i:j + 1]), tree.query_range(i, j))

    def test_update_point(self):
        nums = list(range(1, 6)) + list(range(5, 0, -1))
        tree = segment_tree.SegmentTree(nums)

        for i in range(len(nums)):
            tree.update_point(i, i + 15)
            self.assertEqual(i + 15, tree.query_point(i))
            self.assertEqual(i + 15, tree.query_right(0))

    def test_update_range(self):
        for i in range(4, 0, -1):
            tree = segment_tree.SegmentTree(range(1, 6))
            tree.update_range(i, 4, 0)
            self.assertEqual(i, tree.query_range(0, 4))
