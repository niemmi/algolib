import unittest
import random
from .context import longest_palindromic_substring as lps


def simple(s):
    if not s:
        return 0

    def length(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1

        return r - l - 1

    even = max(length(i, i) for i in range(len(s)))
    odd = max(length(i - 1, i) for i in range(1, len(s)))

    return max(even, odd)


class TestLongestPalindromicSubstring(unittest.TestCase):
    def test_same(self):
        for i in range(10):
            self.assertEqual(i, lps.longest_palindromic_substring('a' * i))

    def test_odd(self):
        self.assertEqual(5 , lps.longest_palindromic_substring('xaxbxac'))

    def test_even(self):
        self.assertEqual(6 , lps.longest_palindromic_substring('xaxbbxac'))

    def test_random(self):
        for i in range(100):
            l = random.randint(3, 20)
            s = ''.join(random.choice('abcd') for _ in range(l))

            self.assertEqual(simple(s), lps.longest_palindromic_substring(s))
