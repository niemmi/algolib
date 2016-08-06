import unittest
import random
import sys
from .context import parallel_sort

MODULE_NAME = 'algolib.sort.parallel_sort'


class TestInsertionSort(unittest.TestCase):
    # Hacks to allow testing with multiprocessing on Python 2
    # http://stackoverflow.com/questions/33128681/how-to-unit-test-code-that-uses-python-multiprocessing
    def setUp(self):
        self.old_main = sys.modules['__main__']
        self.old_main_file = sys.modules['__main__'].__file__
        sys.modules['__main__'] = sys.modules[MODULE_NAME]
        sys.modules['__main__'].__file__ =  sys.modules[MODULE_NAME].__file__

    def tearDown(self):
        sys.modules['__main__'] = self.old_main
        sys.modules['__main__'].__file__ = self.old_main_file

    def test_empty(self):
        res = parallel_sort.sort([])
        self.assertEqual([], res)

    def test_sorted(self):
        res = parallel_sort.sort(range(10))
        self.assertEqual(range(10), res)

    def test_random(self):
        l = random.sample(xrange(1000000), 1000)
        self.assertEqual(sorted(l), parallel_sort.sort(l))
