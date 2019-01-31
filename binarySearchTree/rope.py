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

    def _get_weight(self):
        """ get sum of the lengths of left subtree """
        if self.left is None:
            return 0
        else:
            return self.left.length_sum

    def _index(self, idx):
        """ returns the value at index idx from the subtree of self """
        weight = self._get_weight()
        if weight <= idx:
            return self.right._index(idx - weight)
        if self.left is not None:
            return self.left._index(idx)
        else:
            return self.value[i]

    @classmethod
    def _concat_nodes(cls, left_node, right_node):
        root = cls()
        root.left = left_node
        root.right = right_node
        root.length_sum = left_node.length_sum + right_node.length_sum
        return root

    def _append(self, right_node):
        return self._concat_nodes(self, right_node)
    
    def _append_left(self, left_node):
        return self._concat_nodes(left_node, self)
    
    


class Rope():
    def __init__(self):
        self.root = None

    def index(self, idx):
        """ returns the value at index idx """
        return self.root._index(idx)
    
    @classmethod
    def concat_ropes(cls, left_rope, right_rope):
        """ concatnate two ropes and return a new rope"""
        new_rope = cls()
        new_rope.root = left_rope.root._append(right_rope.root)
        return new_rope
    
    def append(self, right_rope):
        """ append new rope in place """
        self.root = self.root._append(right_rope.root)
    
    def append_left(self, left_rope):
        """ preppend new rope in place """
        self.root = left_rope.root._append(self.root)

    
n1 = Node()
n2 = Node()
Node._concat_nodes(n1, n2)