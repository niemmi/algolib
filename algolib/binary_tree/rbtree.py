"""Red black tree, a self-balanced binary search tree that supports inserts and
reads in O(log n) time no matter what kind of data is inserted. The main target
of implementation has been speed so no custom keys or compare function is
supported.

The comments in insert and remove refer to Wikipedia article:
- https://en.wikipedia.org/wiki/Red%E2%80%93black_tree
"""

from itertools import izip, izip_longest, takewhile
import operator


class Node(object):
    """Tree node.

    Attributes:
        value: Value stored in the node.
        parent: Link to parent.
        red: Boolean value to indicate if node is red or black.
        left: Left child.
        right: Right child.
    """
    def __init__(self, value, parent=None):
        """Constructor.

        Args:
            value: Value to store.
            parent: Link to parent.
        """
        self.value = value
        self.parent = parent
        self.red = True
        self.left = None
        self.right = None

    def __str__(self):
        return '({0},{1},{2},{3})'.format(
            self.value,
            'R' if self.red else 'B',
            self.left,
            self.right
        )

    def __iter__(self):
        """Generator returning nodes in ascending order.

        Yields:
            Nodes in ascending order.
        """
        node = self
        while node:
            yield node.value
            if node.right:
                node = node.right.min()
                continue

            while node.parent and node.parent.right == node:
                node = node.parent

            node = node.parent

    def __reversed__(self):
        """Generator returning nodes in descending order.

        Yields:
            Nodes in descending order.
        """
        node = self
        while node:
            yield node.value
            if node.left:
                node = node.left.max()
                continue

            while node.parent and node.parent.left == node:
                node = node.parent

            node = node.parent

    def min(self):
        """Returns minimum node in tree where this node is a root.

        Returns:
            Node with minimum value.
        """
        node = self
        while node.left:
            node = node.left

        return node

    def max(self):
        """Returns maximum node in tree where this node is a root.

        Returns:
            Node with maximum value.
        """
        node = self
        while node.right:
            node = node.right

        return node

    def rotate_right(self):
        """Right rotation needed to balance tree during insert and removal.

        Moves node down a level in the tree, left child to parent and
        left child's right child to left child.
        """

        # Make parent point to child
        if self.parent:
            if self == self.parent.left:
                self.parent.left = self.left
            else:
                self.parent.right = self.left

        # Make child point to parent
        self.left.parent = self.parent

        # Make child as parent
        self.parent = self.left

        # Switch the child on the node to be rotated
        self.left = self.parent.right
        if self.left:
            self.left.parent = self

        self.parent.right = self

    def rotate_left(self):
        """Left rotation needed to balance tree during insert and removal.

        Moves node down a level in the tree, right child to parent and
        right child's left child to right child.
        """

        # Make parent point to child
        if self.parent:
            if self == self.parent.right:
                self.parent.right = self.right
            else:
                self.parent.left = self.right

        # Make child point to parent
        self.right.parent = self.parent

        # Make child as parent
        self.parent = self.right

        # Switch the child on the node to be rotated
        self.right = self.parent.left
        if self.right:
            self.right.parent = self

        self.parent.left = self

    # Yes they're long but it's also a lot more efficient than spreading code
    # to different methods
    # pylint: disable=too-many-branches, too-many-statements

    @staticmethod
    def insert(root, value):
        """Inserts new value to the tree.

        Args:
            root: Tree root, None if tree is empty.
            value: Value to insert.

        Returns:
            New root node.

        Raise:
            KeyError: If given value is already in the tree.
        """

        # Find parent to insert
        parent = node = root

        while node:
            parent = node
            if value > node.value:
                node = node.right
            elif value < node.value:
                node = node.left
            else:
                # Duplicates aren't supported
                raise KeyError

        # Insert to tree
        node = Node(value, parent)
        if parent:
            if value > parent.value:
                parent.right = node
            else:
                parent.left = node

        while True:
            # Case 1: Stop if node is a root
            if not node.parent:
                node.red = False
                return node

            # Case 2: Stop if parent is black
            if not node.parent.red:
                return root

            # Case 3: If parent and uncle are red paint them black
            #         and grandparent red
            if node.parent.parent:
                if node.parent == node.parent.parent.left:
                    uncle = node.parent.parent.right
                else:
                    uncle = node.parent.parent.left

                if uncle and uncle.red:
                    uncle.red = False
                    node.parent.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent

                    # Back to case 1
                    continue

            break

        # Case 4: Rotate left-right (or r-l) scenario to left-left (or r-r)
        if node == node.parent.right:
            if node.parent == node.parent.parent.left:
                node.parent.rotate_left()
                node = node.left
        elif node == node.parent.left:
            if node.parent == node.parent.parent.right:
                node.parent.rotate_right()
                node = node.right

        # Case 5: Parent is red but uncle black
        if node.parent.parent == root:
            root = node.parent

        node.parent.red = False
        node.parent.parent.red = True
        if node is node.parent.left:
            node.parent.parent.rotate_right()
        else:
            node.parent.parent.rotate_left()

        return root

    @staticmethod
    def remove(root, value):
        """Removes value from the tree.

        Args:
            root: Tree root.
            value: Value to remove.

        Returns:
            New root node, None if tree becomes empty.

        Raise:
            KeyError: If given value is not in the tree.
        """
        node = root

        # Find the node to be removed
        while node:
            if value == node.value:
                break

            node = node.left if value < node.value else node.right

        if not node:
            raise KeyError

        # Make two child case to 1 or 0 child case
        if node.left and node.right:
            child = node.left.max()
            node.value = child.value
            node = child

        # Red node can just be removed
        # Black node with red child can be replaced with recolored child
        child = max(node.left, node.right)
        if node.red or child:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = child
                else:
                    node.parent.right = child

            if child:
                child.parent = node.parent
                child.red = False
            if node == root:
                root = child
            return root

        to_remove = node

        while True:
            # Case 1: Node is root, we're done
            if not node.parent:
                root = node
                break

            if node == node.parent.left:
                sibling = node.parent.right
            else:
                sibling = node.parent.left

            # Case 2: Sibling is red
            # Rotate sibling to replace parent and recolor sibling & parent
            if sibling.red:
                sibling.red = False
                node.parent.red = True
                if node == node.parent.left:
                    sibling = sibling.left
                    node.parent.rotate_left()
                else:
                    sibling = sibling.right
                    node.parent.rotate_right()

                if not node.parent.parent.parent:
                    root = node.parent.parent

            # Case 3: Parent, sibling and sibling's children are all black
            # Recolor sibling as red and move to parent node
            # Case 4: Parent is red but sibling & its' children are black
            # Switch parent and sibling colors
            sl_red = sibling.left and sibling.left.red
            sr_red = sibling.right and sibling.right.red
            if not sl_red and not sr_red:
                sibling.red = True
                if node.parent.red:
                    node.parent.red = False
                    break
                else:
                    node = node.parent
                    continue

            # Case 5: Sibling is black
            # a: s left child is red, right black, node is left child
            # -> rotate s right
            # b: s left child is black, left red, node is right child
            # -> rotate s left
            # After rotation change colors with sibling and the new parent
            if node == node.parent.left and sl_red and not sr_red:
                sibling.rotate_right()
                sibling.red = True
                sibling.parent.red = False
                sibling = sibling.parent
            elif node == node.parent.right and not sl_red and sr_red:
                sibling.rotate_left()
                sibling.red = True
                sibling.parent.red = False
                sibling = sibling.parent

            # Case 6: Sibling is black
            # a: s right child is red, node is left child -> rotate parent left
            # b: s left child is red, node is right child -> rotate parent right
            # Swap colors of sibling & parent and color red node black
            sibling.red, node.parent.red = node.parent.red, sibling.red
            if node == node.parent.left:
                sibling.right.red = False
                node.parent.rotate_left()
            else:
                sibling.left.red = False
                node.parent.rotate_right()

            if not sibling.parent:
                root = sibling
            break

        if to_remove.parent:
            if to_remove == to_remove.parent.left:
                to_remove.parent.left = None
            else:
                to_remove.parent.right = None
        else:
            root = None

        return root
    # pylint: enable=too-many-branches, too-many-statements

class Tree(object):
    """Red black tree.

    Attributes:
        root: Tree root, None if tree is empty.
        size: Tree size.
    """
    def __init__(self, it=()):
        """Constructor.

        Args:
            it: Optional iterable whose elements are added to the tree.

        Raise:
            KeyError: If given iterable contains duplicate values.
        """
        self.root = None
        self.size = 0
        self.insert_iter(it)

    def insert(self, value):
        """Insert value to the tree/

        Args:
            value: Value to insert.

        Raise:
            KeyError: If given value is already in the tree.
        """
        self.root = Node.insert(self.root, value)
        self.size += 1

    def insert_iter(self, it):
        """Inserts all valuebles from given iterable to the tree.

        Args:
            it: Iterable containing values to add.

        Raise:
            KeyError: If given iterable contains duplicate values.
        """
        for value in it:
            self.insert(value)

    def __str__(self):
        return 'Tree([{0}])'.format(', '.join(str(x) for x in self))

    def __delitem__(self, value):
        self.root = Node.remove(self.root, value)
        self.size -= 1

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter((self.root and self.root.min()) or ())

    def __reversed__(self):
        return reversed((self.root and self.root.max()) or ())

    def __contains__(self, item):
        node = self.root
        while node and node.value != item:
            node = node.left if node.value > item else node.right

        return node

    def __nonzero__(self):
        return bool(self.root)

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        fill = object()
        return all(x == y for x, y in izip_longest(self, other, fillvalue=fill))

    def __ne__(self, other):
        return not self == other

    def __diff(self, other):
        for x, y in izip(self, other):
            if x < y:
                return -1
            elif x > y:
                return 1

        return len(self) - len(other)

    def __lt__(self, other):
        return self.__diff(other) < 0

    def __gt__(self, other):
        return self.__diff(other) > 0

    def __le__(self, other):
        return self.__diff(other) <= 0

    def __ge__(self, other):
        return self.__diff(other) >= 0

    def __find_le(self, value):
        res = None
        node = self.root

        while node:
            if node.value < value:
                res = node
                node = node.right
            elif node.value == value:
                return node
            else:
                node = node.left

        return res

    def __find_ge(self, value):
        res = None
        node = self.root

        while node:
            if node.value > value:
                res = node
                node = node.left
            elif node.value == value:
                return node
            else:
                node = node.right

        return res

    def find_le(self, value):
        """Finds greatest value equal or less than given parameter.

        Args:
            value: Value to search for.

        Returns:
            Greatest value equal or less than given value.

        Raises:
            ValueError: If tree doesn't contain value equal or less than given
                parameter.
        """
        res = self.__find_le(value)
        if not res:
            raise ValueError
        return res.value

    def find_ge(self, value):
        """Finds smallest value equal or greater than given parameter.

        Args:
            value: Value to search for.

        Returns:
            Smallest value equal or greater than given value.

        Raises:
            ValueError: If tree doesn't contain value equal or greater than
            given parameter.
        """
        res = self.__find_ge(value)
        if not res:
            raise ValueError
        return res.value

    def min(self):
        """Returns smallest value in the tree.

        Returns:
            Smallest value in the tree.

        Raises:
            ValueError: If tree is empty.
        """
        if not self.root:
            raise ValueError
        return self.root.min().value

    def max(self):
        """Returns greatest value in the tree.

        Returns:
            Greatest value in the tree.

        Raises:
            ValueError: If tree is empty.
        """
        if not self.root:
            raise ValueError
        return self.root.max().value

    def islice(self, start, stop=None, direction=1):
        """Returns iterator that yields all the values between start and stop.

        Args:
            start: Starting value, inclusive
            stop: Optional stop value, excluded from yielded value. By default
                all values are returned.
            direction: Optional, 1 for ascending, -1 for descending

        Returns:
            Iterator that yields values in range defined by the parameters.
        """
        if direction == 1:
            it = self.__find_ge(start) or []
            op = operator.lt
        else:
            it = reversed(self.__find_le(start) or [])
            op = operator.gt

        if stop is None:
            return it
        else:
            return takewhile(lambda x: op(x, stop), it)
