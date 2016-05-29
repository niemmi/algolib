import unittest
import random
from .context import merge_sort


class TestMergeSort(unittest.TestCase):
    def test_empty(self):
        l = []
        res = merge_sort.sort([])
        self.assertEqual([], res)

    def test_sorted(self):
        l = range(10)
        res = merge_sort.sort(l)
        self.assertEqual(range(10), res)

    def test_random(self):
        for i in xrange(1, 100):
            l = random.sample(xrange(1000000), i)
            res = merge_sort.sort(l)
            self.assertEqual(sorted(l), res)

    def test_in_place_empty(self):
        l = []
        merge_sort.sort_in_place([])
        self.assertEqual([], l)

    def test_in_place_sorted(self):
        l = range(10)
        merge_sort.sort_in_place(l)
        self.assertEqual(range(10), l)

    def test_in_place_random(self):
        for i in xrange(1, 100):
            l = random.sample(xrange(1000000), i)
            copy = l[:]
            merge_sort.sort_in_place(l)
            if l != sorted(l):
                print copy
            self.assertEqual(sorted(l), l)

