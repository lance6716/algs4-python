#!/usr/bin/env python3

class RBTree:
    from collections import deque

    class Node:
        RED = True
        BLACK = False
        def __init__(self, key, val, color = RED, size = 1):
            self.key = key
            self.val = val
            self.left = None
            self.right = None
            self.color = color
            self.size = size

    def __init__(self):
        self.root = None

    def _is_red(self, x):
        # rotate may access null as nodes, so we assume it is black
        if x is None:
            return False
        return x.color == RBTree.Node.RED

    def size(self):
        return self._size(self.root)

    def _adjust_size(self, n):
        n.size = 1 + self._size(n.left) + self._size(n.right)

    def _size(self, x):
        if x is None:
            return 0
        return x.size

    def is_empty(self):
        return self.root is None

    def get(self, key):
        return self._get(self.root, key)

    def _get(self, x, key):
        while x is not None:
            if x.key == key:
                return x.val
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        raise ValueError('Key not found')

    def contains(self, key):
        try:
            self.get(key)
            return True
        except ValueError:
            return False

    def put(self, key, val):
        self.root = self._put(self.root, key, val)
        self.root.color = RBTree.Node.BLACK

    def _put(self, x, key, val):
        if x is None:
            return self.Node(key, val)

        if key < x.key:
            x.left = self._put(x.left, key, val)
        elif x.key < key:
            x.right = self._put(x.right, key, val)
        else:
            x.val = val

        # fix-up any right-leaning links
        if self._is_red(x.right) and not self._is_red(x.left):
            x = self._rotate_left(x)
        if self._is_red(x.left) and self._is_red(x.left.left):
            x = self._rotate_right(x)
        if self._is_red(x.left) and self._is_red(x.right):
            self._flip_colors(x)

        self._adjust_size(x)
        return x

    def _rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RBTree.Node.RED # TODO: why?
        x.size = h.size
        self._adjust_size(h)
        return x

    def _rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RBTree.Node.RED
        x.size = h.size
        self._adjust_size(h)
        return x

    def _flip_colors(self, h):
        """
        flip the colors of a node and its two children
        """
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color

    def _move_red_left(self, h):
        """
        Assuming that h is red and both h.left and h.left.left
        are black, make h.left or one of its children red.
        """
        self._flip_colors(h)
        if self._is_red(h.right.left):
            h.right = self._rotate_right(h.right)
            h = self._rotate_left(h)
            self._flip_colors(h)
        return h

    def _move_red_right(self, h):
        """
        Assuming that h is red and both h.right and h.right.left
        are black, make h.right or one of its children red.
        """
        self._flip_colors(h)
        if self._is_red(h.left.left):
            h = self._rotate_right(h)
            self._flip_colors(h)
        return h

    def height(self):
        return self._height(self.root)

    def _height(self, x):
        # a single node is 0-heighted
        if x is None:
            return -1
        return 1 + max(self._height(x.left), self._height(x.right))

    def level_order(self):
        """Return the keys in the BST in level order"""
        keys = []
        queue = self.deque()
        queue.append(self.root)
        while queue:
            x = queue.popleft()
            if x is None:
                continue

            keys.append(x.key)
            queue.append(x.left)
            queue.append(x.right)
        return keys

    def keys(self):
        yield from self._keys(self.root)

    def _keys(self, x):
        if x is None:
            return
        yield from self._keys(x.left)
        yield x.key
        yield from self._keys(x.right)

    def max(self):
        return self._max(self.root).key

    def _max(self, x):
        if x.right is None:
            return x

        return self._max(x.right)

    def min(self):
        return self._min(self.root).key

    def _min(self, x):
        if x.left is None:
            return x

        return self._min(x.left)

    def floor(self, key):
        x = self._floor(self.root, key)
        if x is None:
            return None
        else:
            return x.key

    def _floor(self, x, key):
        if x is None:
            return None
        if x.key == key:
            return x
        elif key < x.key:
            return self._floor(x.left, key)
        t = self._floor(x.right, key)
        if t is not None:
            return t
        else:
            return x

    def ceiling(self, key):
        x = self._ceiling(self.root, key)
        if x is None:
            return None
        else:
            return x.key

    def _ceiling(self, x, key):
        if x is None:
            return None
        if x.key == key:
            return x
        elif x.key < key:
            return self._ceiling(x.right, key)
        t = self._ceiling(x.left, key)
        if t is not None:
            return t
        else:
            return x

    def select(self, k):
        '''
        return key which ranks k
        '''
        if k < 0 or k >= self.size():
            raise ValueError('k should be in range [0, size]')
        return self._select(self.root, k).key

    def _select(self, x, k):
        t = self._size(x.left)
        if k < t:
            return self._select(x.left, k)
        elif t < k:
            return self._select(x.right, k - t - 1)
        else:
            return x

    def rank(self, key):
        return self._rank(self.root, key)

    def _rank(self, x, key):
        if x is None:
            return 0

        if key < x.key:
            return self._rank(x.left, key)
        elif x.key < key:
            return 1 + self._size(x.left) + self._rank(x.right, key)
        else:
            return self._size(x.left)

    def delete(self, key):
        if key is None:
            raise ValueError("argument is null")
        if not self.contains(key):
            return

        # if both children of root are black, set root to red
        if not self._is_red(self.root.left) and not self._is_red(self.root.right):
            self.root.color = RBTree.Node.RED

        self.root = self._delete(self.root, key)
        if not self.is_empty():
            self.root.color = RBTree.Node.BLACK

    def _delete(self, h, key):
        if key < h.key:
            if not self._is_red(h.left) and not self._is_red(h.left.left):
                h = self._move_red_left(h)
            h.left = self._delete(h.left, key)
        else:
            if self._is_red(h.left):
                h = self._rotate_right(h)
            if key == h.key and h.right is None: # means it's leaf, since it's balanced tree
                return None
            if not self._is_red(h.right) and not self._is_red(h.right.left):
                h = self._move_red_right(h)

            if key == h.key:
                x = self._min(h.right)
                h.key = x.key
                h.val = x.val
                h.right = self._delete_min(h.right)
            else:
                h.right = self._delete(h.right, key)

        return self._balance(h)

    def delete_min(self):
        if self.is_empty():
            raise ValueError("BST underflow")

        if not self._is_red(self.root.left) and not self._is_red(self.root.right):
            self.root.color = RBTree.Node.RED

        self.root = self._delete_min(self.root)
        if not self.is_empty():
            self.root.color = RBTree.Node.BLACK

    def _delete_min(self, h):
        if h.left is None:
            return None
        if not self._is_red(h.left) and not self._is_red(h.left.left):
            h = self._move_red_left(h)

        h.left = self._delete_min(h.left)
        return self._balance(h)

    def _balance(self, h):
        if self._is_red(h.right):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)
        self._adjust_size(h)
        return h

if __name__ == '__main__':
    rbtree = RBTree()
    for i in range(10):
        rbtree.put(i, i * 100)
    print(rbtree.get(4))
    for i in range(4, 7):
        rbtree.delete(i)
    print(rbtree.size())
    print(rbtree.rank(9))

    for i in range(0, 20, 2):
        rbtree.put(i, i * 100)
    print(rbtree.ceiling(15))
    print(rbtree.floor(15))
    print(rbtree.height())
    print(list(rbtree.keys()))
    print(rbtree.level_order())
