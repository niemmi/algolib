import unittest
from .context import open_address


# Dummy for ensuring collisions
class Dummy(object):
    def __hash__(self):
        return 1


class TestOpenAddress(unittest.TestCase):
    def test_create(self):
        h = open_address.Hash(xrange(3))
        for i in xrange(3):
            self.assertIn(i, h)

        self.assertNotIn(-1, h)
        self.assertNotIn(3, h)

    def test_len(self):
        h = open_address.Hash()
        for i in xrange(1, 10):
            for j in xrange(10):
                h.add(i)
            self.assertEquals(i, len(h))

    def test_iter(self):
        s = set(xrange(10))
        for x in open_address.Hash(xrange(10)):
            s.remove(x)

        self.assertFalse(s)

    def test_extend(self):
        h = open_address.Hash()
        h.extend(xrange(-2, 10))
        for i in xrange(-2, 10):
            self.assertIn(i, h)

        self.assertNotIn(-3, h)
        self.assertNotIn(10, h)

    def test_collision(self):
        contents = [Dummy() for _ in xrange(10)]
        h = open_address.Hash(contents)
        for x in contents:
            self.assertIn(x, h)

    def test_contains(self):
        l = range(10) + [Dummy() for _ in xrange(2)]
        h = open_address.Hash(l)

        for x in l:
            self.assertIn(x, h)

        for x in (range(-5, 0) + range(10, 15) + [Dummy()]):
            self.assertNotIn(x, h)

    def test_isdisjoint(self):
        h1 = open_address.Hash(xrange(5))
        for i in xrange(-5, 10):
            for j in xrange(i + 1, 10):
                h2 = open_address.Hash(xrange(i, j))
                self.assertEqual(h1.isdisjoint(h2), i >= 5 or j <= 0)

    def test_comparison(self):
        h1 = open_address.Hash(xrange(11))
        h2 = open_address.Hash(xrange(10))

        self.assertFalse(h1 <= h2)
        self.assertFalse(h1 < h2)
        self.assertFalse(h1 == h2)
        self.assertTrue(h1 >= h2)
        self.assertTrue(h1 > h2)
        self.assertTrue(h1 != h2)

        h1.remove(10)

        self.assertTrue(h1 <= h2)
        self.assertFalse(h1 < h2)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 >= h2)
        self.assertFalse(h1 > h2)
        self.assertFalse(h1 != h2)

        h1.remove(9)

        self.assertTrue(h1 <= h2)
        self.assertTrue(h1 < h2)
        self.assertFalse(h1 == h2)
        self.assertFalse(h1 >= h2)
        self.assertFalse(h1 > h2)
        self.assertTrue(h1 != h2)

    def test_and(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                s = set(xrange(i, 10)) & set(xrange(j, 10))
                self.assertEqual(set(h1 & h2), s)

    def test_or(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                s = set(xrange(i, 10)) | set(xrange(j, 10))
                self.assertEqual(set(h1 | h2), s)

    def test_sub(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                s = set(xrange(i, 10)) - set(xrange(j, 10))
                self.assertEqual(set(h1 - h2), s)

    def test_xor(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                s = set(xrange(i, 10)) ^ set(xrange(j, 10))
                self.assertEqual(set(h1 ^ h2), s)

    def test_clear(self):
        h = open_address.Hash(xrange(10))
        h.clear()

        for i in xrange(10):
            self.assertNotIn(i, h)

        self.assertFalse(h)

    def test_pop(self):
        l = range(10) + [Dummy() for _ in xrange(3)]
        h = open_address.Hash(l)

        while h:
            x = h.pop()
            self.assertNotIn(x, h)

        self.assertFalse(h)

    def test_discard(self):
        l = range(10) + [Dummy() for _ in xrange(3)]
        h = open_address.Hash(l)

        for x in l:
            h.discard(x)
            self.assertNotIn(x, h)

        self.assertFalse(h)

        for x in l:
            h.discard(x)

    def test_remove(self):
        l = range(10) + [Dummy() for _ in xrange(3)]
        h = open_address.Hash(l)

        for x in l:
            h.remove(x)
            self.assertNotIn(x, h)

        self.assertFalse(h)

    def test_ior(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                h1 |= h2
                s = set(xrange(i, 10)) | set(xrange(j, 10))
                self.assertEqual(h1, s)

    def test_iand(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                h1 &= h2
                s = set(xrange(i, 10)) & set(xrange(j, 10))
                self.assertEqual(set(h1), s)

    def test_isub(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                h1 -= h2
                s = set(xrange(i, 10)) - set(xrange(j, 10))
                self.assertEqual(set(h1), s)

    def test_ixor(self):
        for i in xrange(10):
            for j in xrange(10):
                h1 = open_address.Hash(xrange(i, 10))
                h2 = open_address.Hash(xrange(j, 10))
                s = set(xrange(i, 10)) ^ set(xrange(j, 10))
                self.assertEqual(set(h1 ^ h2), s)
