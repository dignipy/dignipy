"""BST.py

This module implements vanilla Binary Search Tree

all of the operations(searching, inserting, deleting) takes O(h) time

tree's height: ceil(log(N+1)) <= h <= N 
- best case: full binary tree
- worst case: skewed binary tree

"""

import bst_utils


class Node():
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
    
    def __repr__(self):
        return 'Node({},{})'.format(self.key, repr(self.value))


class BST():
    def __init__(self, key, value):
        self.root = Node(key, value)
        
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
                return node.left
            if node.left is None:
                return node.right
            target = node
            node = self._min(target.right)
            node.right = self._delete_min(target.right)
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

