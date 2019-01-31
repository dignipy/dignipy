# -*- coding: utf-8 -*-
"""fenwickTree.py
This module implements the rope data structure as described in:
    https://en.wikipedia.org/wiki/Rope_(data_structure)
"""

class Node():
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.length = len(value)
        self.weight_sum = len(value)
        self.is_leaf = True
    
    def _get_left_weight_sum(self):
        if self.left is None:
            return 0
        else:
            return self.left.weight_sum


class Rope():
    pass