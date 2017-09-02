import unittest
import random
from .context import heap_sort


class TestInsertionSort(unittest.TestCase):
    def test_empty(self):
        l = []
        heap_sort.sort([])
        self.assertEqual([], l)

    def test_sorted(self):
        l = list(range(10))
        heap_sort.sort(l)
        self.assertEqual(list(range(10)), l)

    def test_random(self):
        for i in range(1, 100):
            l = random.sample(range(1000000), i)
            heap_sort.sort(l)
            self.assertEqual(sorted(l), l)
