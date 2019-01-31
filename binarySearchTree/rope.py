# -*- coding: utf-8 -*-
"""fenwickTree.py
This module implements the rope data structure as described in:
    https://en.wikipedia.org/wiki/Rope_(data_structure)
"""

class Node():
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        # self.length = len(value) # just call len(self.value)
        if value is not None:
            self.length_sum = len(value)
        else:
            self.length_sum = 0


class Rope():
    def __init__(self):
        self.root = None

    def _get_weight(self, node):
        """ get sum of the lengths of left subtree """
        if node.left is None:
            return 0
        else:
            return node.left.length_sum

    def _index(self, node, idx):
        """ returns the value at index idx from the subtree of node """
        weight = self._get_weight(node)
        if weight <= idx:
            return self._index(node.right, idx - weight)
        if node.left is not None:
            return self._index(node.left, idx)
        else:
            return node.value[i]

    def index(self, idx):
        """ returns the value at index idx """
        return self._index(self.root, idx)

    def _concat_nodes(self, left_node, right_node):
        root = Node()
        root.left = left_node
        root.right = right_node
        root.length_sum = left_node.length_sum + right_node.length_sum
        return root

    @classmethod
    def concat(cls, left_rope, right_rope):
        """ concatnate two ropes and return a new rope"""
        new_rope = cls()
        new_rope.root = self._concat_nodes(left_rope.root, right_rope.root)
        return new_rope
    
    def append(self, right_rope):
        """ append a rope in place """
        self.root = self._concat_nodes(self.root, right_rope.root)

    def append_left(self, left_rope):
        """ preppend a rope in place """
        self.root = self._concat_nodes(left_rope.root, self.root)

    
n1 = Node()
n2 = Node()
Node._concat_nodes(n1, n2)