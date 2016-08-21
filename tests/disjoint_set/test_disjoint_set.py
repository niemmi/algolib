from math import ceil, log
from unittest import TestCase
from .context import DisjointSet


class TestDisjointSet(TestCase):
    def test_len(self):
        self.assertEqual(8, len(DisjointSet(xrange(8))))

    def test_find(self):
        ds = DisjointSet(xrange(8))
        window = 1
        while True:
            for i in xrange(0, 8):
                self.assertEqual(ds.find(i - i % window), ds.find(i))
                self.assertTrue(ds.same_component(i - i % window, i))
            window *= 2
            if window > 8:
                break
            for i in xrange(window - 1, 8, window):
                ds.union(i - i % window, i)

    def test_union_updates_size(self):
        ds = DisjointSet(xrange(12))
        for i in xrange(12):
            ds.union(0, i)
            self.assertEqual(i + 1, max(ds._items[j][1] for j in xrange(i + 1)))

    def test_union_limits_height(self):
        ds = DisjointSet(xrange(8))
        window = 1
        while window < 8:
            window *= 2
            for i in xrange(window - 1, 8, window):
                ds.union(i - i % window, i)

        max_height = 0
        for i in xrange(8):
            height = 1
            while ds._items[i][0] != i:
                height += 1
                i = ds._items[i][0]
            max_height = max(max_height, height)

        self.assertLessEqual(int(ceil(log(8, 2))), max_height)
