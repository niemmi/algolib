import unittest
import random
from .context import parallel_sort


class TestParallelSort(unittest.TestCase):
    def test_empty(self):
        res = parallel_sort.sort([])
        self.assertEqual([], res)

    def test_sorted(self):
        res = parallel_sort.sort(range(10))
        self.assertEqual(list(range(10)), res)

    def test_random(self):
        l = random.sample(range(1000000), 1000)
        self.assertEqual(sorted(l), parallel_sort.sort(l))
