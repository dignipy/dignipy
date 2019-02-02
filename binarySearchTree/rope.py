# -*- coding: utf-8 -*-
"""rope.py
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
        """
        get sum of the lengths of left subtree or the length of the leaf
        """
        if node.left is None:
            return node.length_sum
        else:
            return node.left.length_sum

    def _index(self, node, idx):
        """ returns the value at index idx from the subtree of node """
        found_node, node_idx = self._find_index_node(node, idx)
        return found_node[node_idx]

    def _find_index_node(self, node, idx):
        """ returns the node which contains the index idx from the subtree of node"""
        weight = self._get_weight(node)
        if weight <= idx:
            return self._find_index_node(node.right, idx - weight)
        if node.left is not None:
            return self._find_index_node(node.left, idx)
        else:
            return node, idx

    def index(self, idx):
        """ returns the value at index idx """
        found_node, node_idx = self._find_index_node(self.root, idx)
        return found_node[node_idx]

    @classmethod
    def _concat_nodes(cls, left_node, right_node):
        root = Node()
        root.left = left_node
        root.right = right_node
        root.length_sum = left_node.length_sum + right_node.length_sum
        return root

    @classmethod
    def concat(cls, left_rope, right_rope):
        """
        Concatnate two ropes and return a new rope with O(1) time complexity.
        Instead of re-calculating sum of left subtree's length like wikipedia,
        store the length sum of the whole subtree for each node.
        This makes 
        """
        new_rope = cls()
        new_rope.root = cls._concat_nodes(left_rope.root, right_rope.root)
        return new_rope
    
    def append(self, right_rope):
        """ append a rope in place """
        self.root = self._concat_nodes(self.root, right_rope.root)

    def append_left(self, left_rope):
        """ preppend a rope in place """
        self.root = self._concat_nodes(left_rope.root, self.root)
    
    def _split_node(self, node, idx):
        """
        split one node into two with [:idx] and [idx:]
        and return concatenated root node
        """
        left_node = Node(node.value[:idx])
        right_node = Node(node.value[idx:])        
        return self._concat_nodes(left_node, right_node)

    def _traverse_with_condition(self, node, relative_idx, idx):
        """ gather strings from leaf nodes upto relative_idx """
        if relative_idx < 0:
            return []
        weight = self._get_weight(node)
        if node.left is None and node.right is None:
            return [node.value[:relative_idx]]
        else:
            words = self._traverse_with_condition(node.left, relative_idx, idx)
            right_words = self._traverse_with_condition(node.right, relative_idx-weight, idx)
            words.extend(right_words)
            return words

    def text(self, end_idx=None):
        if end_idx is None:
            end_idx = self.root.length_sum
        return ''.join(self._traverse_with_condition(self.root, end_idx, end_idx))

    def _substring(self, node, start, length):
        raise NotImplementedError('substring not finished yet')
        if node.left is None and node.right is None:
            if start == 0 and node.length_sum == length:
                return node
            else:
                return Node(node.value[start:start+length])
                
        if start <= 0 and length >= length(node.left):
            left = node.left
        else:
            left = self._substring(node.left, start, length)
        if (start <= node.left.length_sum) and (start + length >= node.left.length_sum + node.right.length_sum):
            right = ndoe.right
        else:
            right = self._substring(node.right, start-node.left.length_sum, length-left.length_sum)
        return self._concat_nodes(left, right)

    def substring(self, start, length):
        raise NotImplementedError('substring not finished yet')
        new_root = self._substring(self.root, start, length)
        new_rope = self.__class__()
        new_rope.root = new_root
        return new_rope

def example():
    n1 = Node('hel')
    n2 = Node('lo world')
    root = Rope._concat_nodes(n1, n2)
    rope1 = Rope()
    rope1.root = root

    print(rope1.text(7))

    n1 = Node(' my nam')
    n2 = Node('e is')
    root = Rope._concat_nodes(n1, n2)
    rope2 = Rope()
    rope2.root = root

    print(rope2.text(7))

    rope3 = Rope.concat(rope1, rope2)
    print(rope3.text(100))

    n = Node(' minwoo')
    rope4 = Rope()
    rope4.root = n

    rope3.append(rope4)
    print(rope3.text())
    print(rope3.text(19))

    #print(rope3.substring(15, 4).text(), '???')
    
if __name__ == "__main__":
    example()