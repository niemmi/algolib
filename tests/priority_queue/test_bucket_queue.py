from unittest import TestCase
import random
from .context import BucketQueue


class TestBucketQueue(TestCase):
    def test_len(self):
        queue = BucketQueue(zip([1] * 10, range(10)))
        self.assertEqual(10, len(queue))

        queue = BucketQueue(zip(range(10), range(10)))
        self.assertEqual(10, len(queue))

    def test_push(self):
        queue = BucketQueue()
        for i in range(1):
            for j in range(3):
                queue.push(i, i * 10 + j)

        for i in range(1):
            for j in range(3):
                self.assertEqual((i, i * 10 + j), queue.pop())

        self.assertFalse(queue)

    def test_min(self):
        nums = [random.randint(-100, 100) for _ in range(100)]
        queue = BucketQueue(zip(nums, range(len(nums))))
        nums.sort()

        for i in nums:
            self.assertEqual(i, queue.min()[0])
            queue.pop()

    def test_pop(self):
        queue = BucketQueue((-i, i) for i in range(10))
        for i in range(9, -1, -1):
            self.assertEqual((-i, i), queue.pop())

    def test_pop_same_value(self):
        queue = BucketQueue((0, i) for i in range(10))
        self.assertEqual(set(range(10)), {queue.pop()[1] for _ in range(10)})

    def test_change_priority(self):
        values = random.sample(range(100), 20)
        queue = BucketQueue(zip(values[:10] * 10, range(100)))

        for priority, key in zip((v for v in values[10:] for _ in range(10)),
                                 range(100)):
            queue.change_priority(priority, key)

        start = 0
        popped_keys = set()
        for expected_priority in sorted(values[10:]):
            for key in range(start, start + 10):
                priority, key = queue.pop()
                self.assertEqual(expected_priority, priority)
                popped_keys.add(key)

            start += 10
        self.assertEqual(popped_keys, set(range(100)))
