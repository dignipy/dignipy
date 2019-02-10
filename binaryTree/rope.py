# -*- coding: utf-8 -*-
"""rope.py
This module implements the rope data structure as described in:
    https://en.wikipedia.org/wiki/Rope_(data_structure)
"""

# To Do: make delete / replace without rebalancing
# To Do: implement "short" leaf nodes to append short strings to node.value : _concat_ndoes_short
# To Do: make consistent the methods that return the new rope

import bisect
import collections
import heapq
import math


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

    def __repr__(self):
        return 'Node({})'.format(self.value)


class Fibonacci():
    def __init__(self):
        self.sequence = [1, 2]

    def get(self, idx):
        """ get the (idx + 1)-th Fibonacci number"""
        if idx < len(self.sequence):
            return self.sequence[idx]
        new_fib = self.get(idx-1) + self.get(idx-2)
        if idx == len(self.sequence):
            self.sequence.append(new_fib)
        return new_fib

    def find_index(self, number):
        """ returns index idx such that fib(idx) <= number < fib(idx+1) """
        if number < self.sequence[-1]:
            return bisect.bisect(self.sequence, number) - 1
        else:
            while number >= self.sequence[-1]:
                self.get(len(self.sequence))
            return len(self.sequence) - 2


class Rope(collections.abc.MutableSequence):
    def __init__(self, strings=None):
        self.root = None
        if strings is not None:
            if isinstance(strings, str):
                strings = [strings]
            leaves = [Node(value) for value in strings]
            self.rebalance(leaves=leaves)

    def __str__(self):
        return "Rope({})".format(repr(self))

    def __repr__(self):
        """ treat like strings """
        return self.substring()

    def __getitem__(self, idx):
        if isinstance(idx, int):
            # process index as an integer
            length = len(self)
            if -length <= idx < 0:
                idx += length
                return self.index(idx)
            elif 0 <= idx < length:
                return self.index(idx)
            else:
                raise IndexError("index out of range")
        elif isinstance(idx, slice):
            start, stop, step = idx.indices(len(self))  # idx is a slice
            if step == 1:
                return self.substring(start, stop)
            else:
                gather = []
                for i in range(start, stop, step):
                    gather.append(self.index(i))
                return ''.join(gather)
        else:
            raise TypeError("index must be int or slice")

    def __len__(self):
        return self.root.length_sum

    def __setitem__(self, idx, val):
        rope_length = len(self)
        if isinstance(idx, int):
            # process index as an integer
            if -rope_length <= idx < 0:
                idx += rope_length
            elif 0 <= idx < rope_length:
                pass
            else:
                raise IndexError("index out of range")
            start = idx
            stop = idx + 1
            step = 1
        elif isinstance(idx, slice):
            start, stop, step = idx.indices(rope_length)  # idx is a slice
        else:
            raise TypeError("index must be int or slice")
        if step == 1:
            self.replace(start, stop, val)
        else:
            indices_length = len(range(start, stop, step))
            if indices_length != len(val):
                error_message = "attempt to assign sequence of size {}".format(len(val))
                error_message += " to extended slice of size {}".format(indices_length)
                raise ValueError(error_message)
            # To Do: takes too much time rebalancing
            for i, v in zip(range(start, stop, step), val):
                self.__setitem__(i, v)

    def __delitem__(self, idx):
        rope_length = len(self)
        if isinstance(idx, int):
            # process index as an integer
            if -rope_length <= idx < 0:
                idx += rope_length
            elif 0 <= idx < rope_length:
                pass
            else:
                raise IndexError("index out of range")
            start = idx
            stop = idx + 1
            step = 1
        elif isinstance(idx, slice):
            start, stop, step = idx.indices(rope_length)  # idx is a slice
        else:
            raise TypeError("index must be int or slice")
        if step == 1:
            self.delete(start, stop)
        else:
            # To Do: takes too much time rebalancing
            for i in range(start, stop, step):
                self.delete(i, i+1)

    def _get_weight(self, node):
        """
        get sum of the lengths of left subtree or the length of the leaf
        """
        if node.left is None:
            return node.length_sum
        else:
            return node.left.length_sum

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
        if idx < 0 or idx >= self.root.length_sum:
            raise IndexError(idx)
        found_node, node_idx = self._find_index_node(self.root, idx)
        return found_node.value[node_idx]

    @classmethod
    def _concat_nodes(cls, left_node, right_node):
        """ concatenate two nodes and return a new root node"""
        root = Node()
        root.left = left_node
        root.right = right_node
        root.length_sum = left_node.length_sum + right_node.length_sum
        return root

    @classmethod
    def _concat_nodes_short(cls, left_node, right_node):
        """
        concatenate two nodes and return a new root node
        as in the paper, concatenate the strings if:
        a) both nodes are short leaves
        or
        b) the right most son of left_node and the right_node are short leaves
        """
        raise NotImplementedError('short leaf not implemented')
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

    def _substring(self, node, start_idx, end_idx):
        """ gather strings from leaf nodes by index and return as a list """
        if end_idx < 0:
            return []
        weight = self._get_weight(node)
        if node.left is None and node.right is None:
            if start_idx < 0:
                start_idx = 0
            if start_idx == 0 and end_idx == node.length_sum:
                return [node.value]
            else:
                leaf_string = node.value[start_idx:end_idx]
                if leaf_string:
                    return [leaf_string]
                else:
                    return []
        elif start_idx > node.length_sum - 1:
            return []
        else:
            words = self._substring(node.left, start_idx, end_idx)
            right_words = self._substring(node.right, start_idx-weight, end_idx-weight)
            words.extend(right_words)
            return words

    def _sub_leaves(self, node, start_idx, end_idx):
        """ gather leaf nodes by index and return as a list """
        if end_idx < 0:
            return []
        weight = self._get_weight(node)
        if node.left is None and node.right is None:
            if start_idx < 0:
                start_idx = 0
            if start_idx == 0 and end_idx == node.length_sum:
                return [node]
            else:
                leaf_string = node.value[start_idx:end_idx]
                leaf_node = Node(leaf_string) # make new node
                if leaf_string:
                    return [leaf_node]
                else:
                    return []
        elif start_idx > node.length_sum - 1:
            return []
        else:
            leaves = self._sub_leaves(node.left, start_idx, end_idx)
            right_leaves = self._sub_leaves(node.right, start_idx-weight, end_idx-weight)
            leaves.extend(right_leaves)
            return leaves

    def substring(self, start_idx=None, end_idx=None):
        """ substring of the original string, [start_idx: end_idx]"""
        if start_idx is None:
            start_idx = 0
        if end_idx is None:
            end_idx = self.root.length_sum
        elif start_idx < 0:
            raise IndexError(start_idx)
        elif end_idx > self.root.length_sum:
            raise IndexError(end_idx)
        leaves = self._sub_leaves(self.root, start_idx, end_idx)
        return ''.join([node.value for node in leaves])

    def sub_rope(self, start_idx, end_idx):
        """ make and return a new Rope with the substring """
        if start_idx < 0:
            raise IndexError(start_idx)
        elif end_idx > self.root.length_sum:
            raise IndexError(end_idx)
        leaves = self._sub_leaves(self.root, start_idx, end_idx)
        new_rope = self.__class__()
        new_root = self._rebalance(leaves=leaves)
        new_rope.root = new_root
        return new_rope
    
    def split(self, idx):
        """ split the rope into two new ropes """
        left_rope = self.sub_rope(0, idx)
        right_rope = self.sub_rope(idx, self.root.length_sum)
        return left_rope, right_rope
    
    def insert(self, idx, string):
        """ insert string at position idx, returns None """
        self.replace(idx, idx, string)

    def delete(self, i, j):
        """ delete [i:j] entries of rope, returns None """
        left_leaves = self._sub_leaves(self.root, 0, i)
        right_leaves = self._sub_leaves(self.root, j, self.root.length_sum)
        self.rebalance(leaves= left_leaves+right_leaves)

    def replace(self, i, j, string):
        """ replace [i:j] to string, returns None """
        left_leaves = self._sub_leaves(self.root, 0, i)
        middle_leaf = Node(string)
        right_leaves = self._sub_leaves(self.root, j, self.root.length_sum)
        self.rebalance(leaves= left_leaves+[middle_leaf]+right_leaves)

    def build(self, leaves=None):
        """ build a balanced tree from a list of nodes and replace the original root """
        if leaves is None:
            leaves = [n for n in self._traverse(self.root)]
        num_leaves = len(leaves)

        max_depth = int(math.log(num_leaves) / math.log(2)) + 1
        num_last_leaves = 2 * (num_leaves - 2**(max_depth - 1))

        # build tree from bottom to up

        # make a queue for each depth
        q = []
        for i, elem in enumerate(leaves):
            if i < num_last_leaves:
                if i % 2 == 0:
                    prev = elem
                else:
                    left_node = prev
                    right_node = elem
                    node = self._concat_nodes(left_node, right_node)
                    q.append(node)
            else:
                q.append(elem)

        # while depth > 0
        while len(q) > 1:
            tmp_q = []
            for i, node in enumerate(q):
                if i % 2 == 0:
                    prev = node
                else:
                    new_node = self._concat_nodes(prev, node)
                    tmp_q.append(new_node)
            q = tmp_q
        self.root = q[0]
        return self.root

    @classmethod
    def _traverse(cls, node):
        if node is not None:
            if node.left is None and node.right is None:
                # equivalent to checking leaf node
                yield node
            else:
                for n in cls._traverse(node.left):
                    yield n
                for n in cls._traverse(node.right):
                    yield n
        else:
            pass

    def _rebalance(self, leaves=None):
        """
        rebalance the tree from a list of nodes as described in:
        Ropes: an Alternative to Strings, hans-j. boehm, russ atkinson and michael plass, 1995
        and return the new root node
        """
        fib = Fibonacci()
        h = [] # heap
        pos2node = dict()

        if leaves is None:
            nodes = self._traverse(self.root) # generator
        else:
            nodes = leaves

        def fibo_add(node):
            if not h or h[0] > node.length_sum:
                pos = fib.find_index(node.length_sum)
                heapq.heappush(h, pos)
                pos2node[pos] = node
            else:
                pos = heapq.heappop(h)
                old_node = pos2node[pos]
                concat_node = self._concat_nodes(old_node, node)
                del pos2node[pos]
                fibo_add(concat_node)

        for node in nodes:
            fibo_add(node)

        right_pos = heapq.heappop(h)
        right_node = pos2node[right_pos]
        del pos2node[right_pos]
        while len(h) >= 1:
            left_pos = heapq.heappop(h)
            left_node = pos2node[left_pos]
            right_node = self._concat_nodes(left_node, right_node)
            del pos2node[left_pos]
        return right_node

    def rebalance(self, leaves=None):
        """ rebalance the rope with the given leaf nodes and replace the root """
        root = self._rebalance(leaves=leaves)
        self.root = root

def example():
    rope1 = Rope(['hel', 'lo world'])
    print(rope1[0:7])

    rope2 = Rope([' my nam', 'e is'])
    print(rope2[0:7])

    rope3 = Rope.concat(rope1, rope2)
    print(rope3)

    rope4 = Rope(' minwoo')
    rope3.append(rope4)
    print()
    print(rope3)
    rope3.rebalance()

    for leaf in rope3._traverse(rope3.root):
        print(leaf)
    print()
    sub_rope = rope3.sub_rope(1, 14)
    substring = rope3[1:14]
    print(sub_rope, '==', substring)
    print('equal?', sub_rope == substring)

    del rope3[1:14]  # __delitem__
    print(rope3)

    rope3[1:1] = repr(sub_rope)  # insert
    print(rope3)

    rope3[::-1] = 'HELLO WORLD MY NAME IS OOMNIW'  # __setitem__
    print(rope3)
    
    
    import time
    start1 = time.time()
    a = 'a'*10000
    b = str(a)
    for _ in range(100):
        b = b[:int(len(b)/2)] + a + b[int(len(b)/2):]
    end1 = time.time()
    print("string append time:", end1 - start1)
    start2 = time.time()
    b = Rope([a])
    print(len(b))
    for i in range(496):
        b.insert(int(len(b)/2), Rope([a]))
    print('no problem')
    end2 = time.time()
    print('found a bug')
    b.insert(int(len(b)/2), Rope([a]))

    print("rope append time:", end2 - start2)
    

if __name__ == "__main__":
    example()
