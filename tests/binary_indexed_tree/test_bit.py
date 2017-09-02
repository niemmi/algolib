import unittest
from .context import bit


class TestBIT(unittest.TestCase):
    def test_create(self):
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        expected = [0, 1, 3, 3, 10, 5, 11, 7, 36]
        for i in range(1, len(nums) + 1):
            src = nums[:i]
            bit.create(src)
            self.assertEqual(expected[:i], src, 'Should create BIT')

    def test_get(self):
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        bit.create(nums)
        for i in range(1, len(nums)):
            self.assertEqual(i, bit.query_point(nums, i),
                             'Should return correct num')

    def test_query(self):
        nums = list(range(9))
        bit.create(nums)
        for i in range(1, len(nums)):
            self.assertEqual(i * (i + 1) // 2, bit.query_left(nums, i),
                             'Should return sum')

    def test_query_range(self):
        nums = list(range(9))
        tree = nums[:]
        bit.create(tree)
        for i in range(1, len(nums)):
            for j in range(i, len(nums)):
                self.assertEqual(sum(nums[i:j + 1]),
                                 bit.query_range(tree, i, j),
                                 'Should return range')

    def test_update(self):
        nums = list(range(9))
        bit.create(nums)
        for i in range(1, len(nums)):
            bit.update_point(nums, i, 1)
            for j in range(1, len(nums)):
                exp = j + int(j <= i)
                self.assertEqual(exp, bit.query_point(nums, j),
                                 'Should have incremented')

    def test_contains(self):
        nums = list(range(9))
        t = nums[:]
        bit.create(t)
        for i in range(1, len(nums)):
            x = sum(nums[:i + 1])
            self.assertFalse(bit.contains(t, x - 1), 'Should return False')
            self.assertTrue(bit.contains(t, x), 'Should return True')
            self.assertFalse(bit.contains(t, x + 1), 'Should return False')

        self.assertFalse(bit.contains(t, 0))
        self.assertFalse(bit.contains(t, 1000))

    def test_bisect_left(self):
        # Test with uniques
        for i in range(1, 10):
            nums = list(range(i))
            t = nums[:]
            bit.create(t)
            self.assertEqual(1, bit.bisect_left(t, 0),
                             'Should return first index')
            self.assertEqual(len(nums), bit.bisect_left(t, sum(nums) + 1),
                             'Should return length')
            for j in range(1, len(nums)):
                to_find = sum(nums[:j + 1])
                self.assertEqual(j, bit.bisect_left(t, to_find - 1),
                                 'Should return index')
                self.assertEqual(j, bit.bisect_left(t, to_find),
                                 'Should return index')
                self.assertEqual(j + 1, bit.bisect_left(t, to_find + 1),
                                 'Should return index')

        # Test with duplicates
        for i in range(8):
            nums = [0, 1] + [0] * i + [1]
            bit.create(nums)
            self.assertEqual(1, bit.bisect_left(nums, 1), 'Should return start')
            self.assertEqual(i + 2, bit.bisect_left(nums, 2),
                             'Should return 2nd last')
            self.assertEqual(len(nums), bit.bisect_left(nums, 3),
                             'Should return end')

    def test_bisect_right(self):
        # Test with uniques
        for i in range(1, 10):
            nums = list(range(i))
            t = nums[:]
            bit.create(t)
            self.assertEqual(1, bit.bisect_right(t, 0),
                             'Should return first index')
            self.assertEqual(len(nums), bit.bisect_right(t, sum(nums) + 1),
                             'Should return last length')
            for j in range(1, len(nums)):
                to_find = sum(nums[:j + 1])
                self.assertEqual(j, bit.bisect_right(t, to_find - 1),
                                 'Should return index')
                self.assertEqual(j + 1, bit.bisect_right(t, to_find),
                                 'Should return following index')
                self.assertEqual(j + 1, bit.bisect_right(t, to_find),
                                 'Should return following index')

        # Test with duplicates
        for i in range(8):
            nums = [0, 1] + [0] * i
            bit.create(nums)
            self.assertEqual(1, bit.bisect_right(nums, 0),
                             'Should return start')
            self.assertEqual(len(nums), bit.bisect_right(nums, 1),
                             'Should return end')
