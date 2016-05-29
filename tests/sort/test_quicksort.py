import unittest
import random
from .context import quicksort


class TestInsertionSort(unittest.TestCase):
    def test_empty(self):
        l = []
        quicksort.sort([])
        self.assertEqual([], l)

    def test_sorted(self):
        l = range(10)
        quicksort.sort(l)
        self.assertEqual(range(10), l)

    def test_random(self):
        for i in xrange(1, 100):
            l = random.sample(xrange(1000000), i)
            quicksort.sort(l)
            self.assertEqual(sorted(l), l)
