from unittest import TestCase
from random import sample, shuffle
from .context import BinaryHeap


class TestBinaryHeap(TestCase):
    def test_len(self):
        heap = BinaryHeap(zip(xrange(10), xrange(10)))
        self.assertEqual(10, len(heap))

    def test_push(self):
        heap = BinaryHeap()
        for i in xrange(10):
            heap.push(i, i)
        for i in xrange(19, 9, -1):
            heap.push(i, i)

        self.assertEqual(range(20), [heap.pop()[0] for _ in xrange(20)])

    def test_min(self):
        test_data = range(-10, 10)
        shuffle(test_data)
        heap = BinaryHeap((i, i + 5) for i in test_data)
        self.assertEqual((-10, -5), heap.min())

    def test_pop(self):
        heap = BinaryHeap((i, -i) for i in xrange(10))
        for i in xrange(9, -1, -1):
            self.assertEqual((i, -i), heap.pop())

    def test_pop_same_value(self):
        heap = BinaryHeap((i, 0) for i in xrange(10))
        self.assertEqual(set(xrange(10)), {heap.pop()[0] for _ in xrange(10)})

    def test_push_pop(self):
        heap = BinaryHeap((i, i) for i in xrange(0, 10, 2))
        self.assertEqual((0, 0), heap.push_pop(5, 5))
        self.assertEqual((0, 0), heap.push_pop(0, 0))
        self.assertEqual((2, 2), heap.push_pop(10, 10))
        self.assertEqual([4, 5, 6, 8, 10],
                         [heap.pop()[1] for _ in xrange(len(heap))])

    def test_replace(self):
        heap = BinaryHeap((i, i) for i in xrange(10))
        self.assertEqual((0, 0), heap.replace(-1, -1))
        self.assertEqual((-1, -1), heap.replace(10, 10))
        self.assertEqual(range(1, 11),
                         [heap.pop()[0] for _ in xrange(len(heap))])

    def test_change_value(self):
        values = sample(xrange(100), 20)
        heap = BinaryHeap(zip(xrange(10), values[:10]))

        for k, v in zip(xrange(10), values[10:]):
            heap.change_value(k, v)

        self.assertEqual(sorted(range(10), key=lambda x: values[x + 10]),
                         [heap.pop()[0] for _ in xrange(len(heap))])

