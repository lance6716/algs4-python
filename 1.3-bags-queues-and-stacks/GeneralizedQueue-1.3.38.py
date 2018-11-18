#!/usr/bin/env python3

class RBTree:
    """Left leaning RBTree based to achieve logarithmic insert/delete"""
    class Node:
        def __init__(self, key, value, N=1, red=True):
            """N is the number of nodes(include itself) in this subtree
            red indicate the edge to this node is color red, in other words,
            an inner horizontal line of 3-node
            """
            self.key = key
            self.value = value
            self.N = N
            self.red = red
            self.left = None
            self.right = None

        def __str__(self):
            return f'key: {self.key}, value: {self.value}, N: {self.N}, red: {self.red}'

    def __init__(self):
        self.root = None

    def _is_red(self, n):
        if n is None:
            return False
        return n.red

    def _size(self, n):
        if n is None:
            return 0
        return n.N

    def _rotate_left(self, n):
        x = n.right
        n.right = x.left
        x.left = n

        x.red = n.red
        n.red = True

        x.N = n.N
        n.N = 1 + self._size(n.left) + self._size(n.right)
        return x

    def _rotate_right(self, n):
        x = n.left
        n.left = x.right
        x.right = n

        x.red = n.red
        n.red = True

        x.N = n.N
        n.N = 1 + self._size(n.left) + self._size(n.right)
        return x

    def _flip_color(self, n):
        n.red = not n.red
        n.left.red = not n.left.red
        n.right.red = not n.right.red

    def put(self, key, val):
        self.root = self._put(self.root, key, val)
        self.root.red = False # nonesense, only for convection

    def _put(self, node, key, val):
        if node is None:
            return self.Node(key, val)

        if key == node.key:
            node.value = val
        elif key < node.key:
            node.left = self._put(node.left, key, val)
        else:
            node.right = self._put(node.right, key, val)

        if self._is_red(node.right) and not self._is_red(node.left):
            node = self._rotate_left(node)
        if self._is_red(node.left) and self._is_red(node.left.left):
            node = self._rotate_right(node)
        if self._is_red(node.left) and self._is_red(node.right):
            self._flip_color(node)

        node.N = 1 + self._size(node.left) + self._size(node.right)
        return node

    def _move_red_left(self, n):
        '''in 2-3-4 tree logical view, make left child a 3-or-4 node'''
        self._flip_color(n) # make left most key in n a level down,
                            # conbine it with n.left and n.second-left
        if self._is_red(n.right.left): # if n.second-left is not a 2-node
                                       # we made a 5-node and should adjust
            n.right = self._rotate_right(n.right)
            n = self._rotate_left(n)
            self._flip_color(n)
        return n

    def _move_red_right(self, n):
        '''make right child a 3-or-4 node, but maybe right leaning
        but a right-node deletion will be performed, it doesn't matter
        to break left leaning
        '''
        self._flip_color(n)
        if self._is_red(n.left.left):
            n = self._rotate_right(n)
            self._flip_color(n)
        return n

    def _balance(self, n):
        if self._is_red(n.right):
            n = self._rotate_left(n)
        if self._is_red(n.left) and self._is_red(n.left.left):
            n = self._rotate_right(n)
        if self._is_red(n.left) and self._is_red(n.right):
            self._flip_color(n)

        n.N = 1 + self._size(n.left) + self._size(n.right)
        return n

    def _delete_min(self, n):
        if n.left is None:
            return None

        if not self._is_red(n.left) and not self._is_red(n.left.left):
            n = self._move_red_left(n)

        n.left = self._delete_min(n.left) # for a 4-node imply, both 
                                          # children are red, this deletion
                                          # causes a right-lean red link,
                                          # thus need _balance first 
                                          # if-clause
        return self._balance(n)

    def delete_min(self):
        if not (self._is_red(self.root.left)
                and not self._is_red(self.root.right)):
            self.root.red = True

        self.root = self._delete_min(self.root)
        if self.root is not None:
            self.root.red = False

    def _min(self, n):
        if n.left is None:
            return n
        else:
            return self._min(n.left)

    def _delete(self, n, key):
        if key < n.key:
            if not self._is_red(n.left) and not self._is_red(n.left.left):
                n = self._move_red_left(n)
            n.left = self._delete(n.left, key)
        else: # equals or greater than
            if self._is_red(n.left):      # prepare for greater than. if 
                n = self._rotate_right(n) # equals n.key and not bottom, 
                                          # we will perform deletion in 
                                          # right subtree, so the root of 
                                          # sub tree should be red. Same
                                          # reason for following 
                                          # _move_red_right.
            if key == n.key and n.right is None:
                return None
            if (not self._is_red(n.right) 
                and not self._is_red(n.right.left)):
                n = self._move_red_right(n)
            if key == n.key:
                x = self._min(n.right)
                n.key = x.key
                n.value = x.value
                n.right = self._delete_min(n.right)
            else:
                n.right = self._delete(n.right, key)
        return self._balance(n)

    def delete(self, key):
        if not (self._is_red(self.root.left)
                and not self._is_red(self.root.right)):
            self.root.red = True

        self.root = self._delete(self.root, key) # TODO: key not in tree?
        if self.root is not None:
            self.root.red = False

    def _delete_rank(self, n, k):
        if n is None:
            raise ValueError('k not legal')

        if n.left is None:
            if k == 1:
                ret = n.value
                self.delete(n.key)
                return ret
            else:
                raise ValueError('I guess this will not happen')

        if k == n.left.N + 1:
            ret = n.value
            self.delete(n.key)
            return ret

        if k < n.left.N + 1:
            return self._delete_rank(n.left, k)
        else:
            return self._delete_rank(n.right, k - 1 - n.left.N)

    def delete_rank(self, k):
        return self._delete_rank(self.root, k)

    def debug(self):
        def foo(n):
            if n.left:
                foo(n.left)
            print(n)
            if n.right:
                foo(n.right)

        if self.root:
            foo(self.root)
        else:
            print('tree is empty')

class GeneralizedQueue:
    def __init__(self):
        self.tree = RBTree()
        self._counter = 0

    def empty(self):
        return self.tree.root is None

    def insert(self, val):
        self.tree.put(self._counter, val)
        self._counter += 1

    def delete(self, k):
        return self.tree.delete_rank(k)

if __name__ == '__main__':
    # tree = RBTree()
    # for i in range(8):
    #     tree.put(i, i + 10)
    # tree.put(4, 44)
    # tree.delete_min()
    # tree.delete(6)
    # tree.debug()
    q = GeneralizedQueue()
    for i in range(10):
        q.insert(i)
    
    print(q.delete(3))
    print(q.delete(3))
    print(q.delete(1))
    print(q.delete(4))
