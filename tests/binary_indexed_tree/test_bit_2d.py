import unittest
from .context import bit_2d


class TestBIT(unittest.TestCase):
    def test_create(self):
        grid = [[0, 0, 0, 0, 0]]
        grid += [[0] + [1] * 4 for _ in xrange(4)]
        expected = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 1, 4],
            [0, 2, 4, 2, 8],
            [0, 1, 2, 1, 4],
            [0, 4, 8, 4, 16]
        ]
        bit_2d.create(grid)
        self.assertEqual(expected, grid, 'Should create 2D BIT')

    def test_query_point(self):
        grid = [[0] * 5 for _ in xrange(5)]

        for i in xrange(4):
            for j in xrange(4):
                bit_2d.update_point(grid, i + 1, j + 1, i * 4 + j)

        for i in xrange(4):
            for j in xrange(4):
                self.assertEqual(i * 4 + j,
                                 bit_2d.query_point(grid, i + 1, j + 1),
                                 'Should return cell number')

    def test_query_top_left(self):
        grid = [[0] * 5 for _ in xrange(5)]

        for i in xrange(4):
            for j in xrange(4):
                bit_2d.update_point(grid, i + 1, j + 1, i * 4 + j)

        self.assertEqual(6, bit_2d.query_top_left(grid, 1, 4))
        self.assertEqual(28, bit_2d.query_top_left(grid, 2, 4))
        self.assertEqual(66, bit_2d.query_top_left(grid, 3, 4))

    def test_query_range_2d(self):
        grid = [[0] * 5 for _ in xrange(5)]

        for i in xrange(4):
            for j in xrange(4):
                bit_2d.update_point(grid, i + 1, j + 1, i * 4 + j)

        for start_y in xrange(4):
            for end_y in xrange(start_y, 4):
                for start_x in xrange(4):
                    for end_x in xrange(start_x, 4):
                        first = start_y * 4 + start_x
                        last = end_y * 4 + end_x
                        exp = (end_x - start_x + 1) * (end_y - start_y + 1)
                        exp *= (first + last)
                        exp /= 2
                        res = bit_2d.query_range(grid, start_y + 1, start_x + 1,
                                                 end_y + 1, end_x + 1)
                        self.assertEqual(exp, res, 'Should return sum')

    def test_update_point(self):
        grid = [[0] * 5 for _ in xrange(5)]
        expected = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 1, 4],
            [0, 2, 4, 2, 8],
            [0, 1, 2, 1, 4],
            [0, 4, 8, 4, 16]
        ]

        for y in xrange(1, 5):
            for x in xrange(1, 5):
                bit_2d.update_point(grid, y, x, 1)

        self.assertEqual(expected, grid, 'Should be updated')
