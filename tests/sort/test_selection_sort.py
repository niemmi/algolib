import unittest
import random
from .context import selection_sort


class TestSelectionSort(unittest.TestCase):
    def test_empty(self):
        l = []
        selection_sort.sort([])
        self.assertEqual([], l)

    def test_sorted(self):
        l = list(range(10))
        selection_sort.sort(l)
        self.assertEqual(list(range(10)), l)

    def test_random(self):
        for i in range(1, 100):
            l = random.sample(range(1000000), i)
            selection_sort.sort(l)
            self.assertEqual(sorted(l), l)
