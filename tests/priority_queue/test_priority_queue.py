from unittest import TestCase
from random import sample, shuffle
from .context import PriorityQueue


class TestBinaryQueue(TestCase):
    def test_len(self):
        queue = PriorityQueue(zip(xrange(10), xrange(10)))
        self.assertEqual(10, len(queue))

    def test_push(self):
        queue = PriorityQueue()
        for i in xrange(10):
            queue.push(i, i)
        for i in xrange(19, 9, -1):
            queue.push(i, i)

        self.assertEqual(range(20), [queue.pop()[0] for _ in xrange(20)])

    def test_min(self):
        test_data = range(-10, 10)
        shuffle(test_data)
        queue = PriorityQueue((i, i + 5) for i in test_data)
        self.assertEqual((-10, -5), queue.min())

    def test_pop(self):
        queue = PriorityQueue((-i, i) for i in xrange(10))
        for i in xrange(9, -1, -1):
            self.assertEqual((-i, i), queue.pop())

    def test_pop_same_value(self):
        queue = PriorityQueue((0, i) for i in xrange(10))
        self.assertEqual(set(xrange(10)), {queue.pop()[1] for _ in xrange(10)})

    def test_push_pop(self):
        queue = PriorityQueue((i, i) for i in xrange(0, 10, 2))
        self.assertEqual((0, 0), queue.push_pop(5, 5))
        self.assertEqual((0, 0), queue.push_pop(0, 0))
        self.assertEqual((2, 2), queue.push_pop(10, 10))
        self.assertEqual([4, 5, 6, 8, 10],
                         [queue.pop()[1] for _ in xrange(len(queue))])

    def test_replace(self):
        queue = PriorityQueue((i, i) for i in xrange(10))
        self.assertEqual((0, 0), queue.replace(-1, -1))
        self.assertEqual((-1, -1), queue.replace(10, 10))
        self.assertEqual(range(1, 11),
                         [queue.pop()[0] for _ in xrange(len(queue))])

    def test_change_priority(self):
        values = sample(xrange(100), 20)
        queue = PriorityQueue(zip(values[:10], xrange(10)))

        for priority, key in zip(values[10:], xrange(10)):
            queue.change_priority(priority, key)

        self.assertEqual(sorted(range(10), key=lambda x: values[x + 10]),
                         [queue.pop()[1] for _ in xrange(len(queue))])

