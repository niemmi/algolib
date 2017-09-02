import unittest
from .context import rbtree
from itertools import zip_longest
from random import shuffle


class TestNode(unittest.TestCase):
    SIZE = 100

    def setUp(self):
        nums = list(range(self.SIZE))
        shuffle(nums)
        self.root = rbtree.Node(nums[0])
        for num in nums[1:]:
            node = self.root
            while node:
                parent = node
                node = node.left if num < node.value else node.right

            if num < parent.value:
                parent.left = rbtree.Node(num, parent)
            else:
                parent.right = rbtree.Node(num, parent)

    def test_min(self):
        self.assertEqual(0, self.root.min().value)

    def test_max(self):
        self.assertEqual(self.SIZE - 1, self.root.max().value)


class TestInsertRemove(unittest.TestCase):
    SIZE = 10000

    def setUp(self):
        self.data = list(range(self.SIZE))
        self.tree = rbtree.Tree()
        shuffle(self.data)

    def test_insert_node(self):
        for item in self.data:
            self.tree.insert(item)

        for exp, val in zip_longest(range(self.SIZE), self.tree):
            self.assertEqual(exp, val)

    def test_remove_node(self):
        self.tree.extend(self.data)

        for val in range(self.SIZE):
            self.assertTrue(val in self.tree)
            del self.tree[val]
            self.assertFalse(val in self.tree)


class TestTree(unittest.TestCase):
    SIZE = 100

    def setUp(self):
        data = list(range(self.SIZE))
        shuffle(data)
        self.tree = rbtree.Tree(data)

    def test_insert_tree(self):
        self.assertFalse(self.SIZE in self.tree)
        self.tree.insert(self.SIZE)
        self.assertTrue(self.SIZE in self.tree)

    def test_len_tree(self):
        self.assertEqual(self.SIZE, len(self.tree))
        for x in range(self.SIZE):
            del self.tree[x]
        self.assertEqual(0, len(self.tree))

    def test_str_tree(self):
        self.assertEqual('Tree({0})'.format(list(range(5))),
                         str(rbtree.Tree(range(5))))

    def test_del_contains_tree(self):
        for val in range(self.SIZE):
            self.assertTrue(val in self.tree)
            del self.tree[val]
            self.assertFalse(val in self.tree)

    def test_iter_tree(self):
        self.assertEqual([], list(rbtree.Tree()))
        self.assertEqual(list(self.tree), list(range(self.SIZE)))

    def test_reversed_tree(self):
        self.assertEqual([], list(reversed(rbtree.Tree())))
        self.assertEqual(list(reversed(self.tree)),
                         list(range(self.SIZE - 1, -1, -1)))

    def test_nonzero_tree(self):
        for val in range(self.SIZE):
            self.assertTrue(self.tree)
            del self.tree[val]

        self.assertFalse(self.tree)

    def test_eq_ne_tree(self):
        self.assertNotEqual(self.tree, rbtree.Tree())
        self.assertNotEqual(self.tree, rbtree.Tree(range(self.SIZE - 1)))
        self.assertEqual(self.tree, rbtree.Tree(range(self.SIZE)))
        self.assertNotEqual(self.tree, rbtree.Tree(range(self.SIZE + 1)))

    def test_lt_le_tree(self):
        tree = rbtree.Tree(range(99))
        self.assertLess(tree, self.tree)
        self.assertLessEqual(tree, self.tree)
        tree.insert(99)
        self.assertLessEqual(tree, self.tree)
        tree.insert(100)
        self.assertLess(self.tree, tree)
        self.assertLessEqual(self.tree, tree)
        del self.tree[99]
        self.assertLess(self.tree, tree)
        self.assertLessEqual(self.tree, tree)

    def test_gt_ge_tree(self):
        tree = rbtree.Tree(range(99))
        self.assertGreater(self.tree, tree)
        self.assertGreaterEqual(self.tree, tree)
        tree.insert(99)
        self.assertGreaterEqual(self.tree, tree)
        tree.insert(100)
        self.assertGreater(tree, self.tree)
        self.assertGreaterEqual(tree, self.tree)
        del self.tree[99]
        self.assertGreater(tree, self.tree)
        self.assertGreaterEqual(tree, self.tree)


class TestFind(unittest.TestCase):
    MAX = 200

    def setUp(self):
        self.tree = rbtree.Tree(range(0, self.MAX + 1, 2))

    def test_find_le(self):
        self.assertRaises(ValueError, lambda: self.tree.find_le(-1))
        for i in range(0, self.MAX + 2):
            self.assertEqual(i - i % 2, self.tree.find_le(i))

    def test_find_ge(self):
        self.assertRaises(ValueError, lambda: self.tree.find_ge(self.MAX + 1))
        for i in range(-1, self.MAX + 1):
            self.assertEqual(i + i % 2, self.tree.find_ge(i))

    def test_min_tree(self):
        self.assertEqual(0, self.tree.min())

    def test_max_tree(self):
        self.assertEqual(self.MAX, self.tree.max())

    def test_islice_tree(self):
        self.assertEqual(list(range(0, self.MAX + 1, 2)),
                         list(self.tree.islice(0)))
        self.assertEqual(list(range(0, self.MAX + 1, 2)),
                         list(self.tree.islice(-10)))
        self.assertEqual(list(range(10, 20, 2)),
                         list(self.tree.islice(10, 20)))
        self.assertEqual(list(range(20, 10, -2)),
                         list(self.tree.islice(20, 10, -1)))
