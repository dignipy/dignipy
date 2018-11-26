# -*- coding: utf-8 -*-
"""BST.py

This module implements vanilla Binary Search Tree

all of the operations(searching, inserting, deleting) takes O(h) time

tree's height: ceil(log(N+1)) <= h <= N
- best case: full binary tree
- worst case: skewed binary tree

"""

import collections
from collections import abc
import bst_utils


class Node():
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return 'Node({},{})'.format(self.key, repr(self.value))


class BST(abc.MutableMapping):
    def __init__(self, key, value):
        self.root = Node(key, value)
        self._len = 1  # the root

    def _key_check(self, key):
        """ check key type and raise error if not valid"""
        if isinstance(key, int) or isinstance(key, float):
            pass
        else:
            raise TypeError("a BST key must be a number")

    def __getitem__(self, key):
        self._key_check(key)
        item = self._search(self.root, key)
        return item

    def __setitem__(self, key, value):
        self._key_check(key)
        self._insert(self.root, key, value)

    def __delitem__(self, key):
        self._key_check(key)
        self.root = self._delete(self.root, key)

    def __iter__(self):
        """iterate over keys preorder"""
        iter_queue = collections.deque()
        iter_queue.append(self.root)
        while iter_queue:
            node = iter_queue.popleft()
            yield node.key
            if node.left is not None:
                iter_queue.append(node.left)
            if node.right is not None:
                iter_queue.append(node.right)

    def __len__(self):
        return self._len

    def search(self, key):
        """get the value of a matched node"""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key < node.key:
            return self._search(node.left, key)
        elif key > node.key:
            return self._search(node.right, key)
        else:
            return node.value

    def insert(self, key, value):
        """insert a new node, or update the value of existed node"""
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            self._len += 1
            # make new node
            return Node(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        return node

    def min(self):
        """get a node which has the minimum key"""
        if self.root is None:
            return None
        return self._min(self.root)

    def _min(self, node):
        if node.left is None:
            return node
        return self._min(node.left)

    def delete_min(self):
        """delete a node which has the minimum key"""
        if self.root is None:
            print("Empty Tree")
        self.root = self._delete_min(self.root)

    def _delete_min(self, node):
        if node.left is None:
            # last node
            self._len -= 1
            if node.right is None:
                return None
            else:
                return node.right
        node.left = self._delete_min(node.left)
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """
        case 0: target node has no child
        case 1: target node has one child(left or right)
        case 2: target node has two children(left and right)
        """
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.right is None:
                self._len -= 1
                return node.left
            elif node.left is None:
                self._len -= 1
                return node.right
            else:
                target = node
                node = self._min(target.right)
                node.right = self._delete_min(target.right)
                # _len decreased
                node.left = target.left
        return node


if __name__ == '__main__':
    """test"""
    bst = BST(12, 'A')
    bst.insert(10, 'B')
    bst.insert(15, 'C')
    bst.insert(16, 'D')
    bst.insert(5, 'E')
    bst.insert(14, 'F')

    print('after insertion')

    bst_utils.in_order(bst.root)

    bst.delete_min()
    print('after deleting min')
    bst_utils.in_order(bst.root)

    bst.delete(12)
    print('after delete 12')
    bst_utils.in_order(bst.root)

    print()
    print('----new test----')
    print()
    bst = BST(12, 'a')
    bst[10] = 'b'
    bst[15] = 'c'
    bst[16] = 'd'
    bst[5] = 'e'
    bst[14] = 'f'

    print('after insertion')
    print('size', len(bst))

    bst_utils.in_order(bst.root)

    bst.delete_min()
    print('after deleting min')
    print('size', len(bst))
    bst_utils.in_order(bst.root)

    del bst[12]
    print('after delete 12')
    print('size', len(bst))
    bst_utils.in_order(bst.root)

