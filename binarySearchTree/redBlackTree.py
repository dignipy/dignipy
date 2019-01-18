"""redBlackTree.py

This module implements Left-Leaning Red-Black Tree (LLRB)

insertion & deletion takes only O(h) time 
- [TODO] implement delete() using delete_min()

height of the RBT(N nodes) is not bigger than 2logN
- if there are no RED nodes in the tree, h = logN
- if it has the maximum RED nodes, h <= 2logN
"""

import bst_utils


"""constant"""
RED = True
BLACK = False


class Node():
    def __init__(self, key, value, color):
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None
    
    def __repr__(self):
        color = 'RED'
        if self.color == BLACK:
            color = 'BLACK'
        return  'Node({},{},{})'.format(self.key, repr(self.value), color)
		

class RedBlackTree():
    def __init__(self):
        self.root = None
    
    def is_empty(self):
        return self.root is None
    
    def is_red(self, node):
        if node is None:
            return False
        return node.color == RED
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        searched, parent = self._search_node(node, key)
        if searched is None:
            return None
        else:
            return searched.value

    def _search_node(self, node, key, parent=None):
        if node is None:
            return None, None
        if key < node.key:
            return self._search(node.left, key, parent=node)
        elif key > node.key:
            return self._search(node.right, key, parent=node)
        else:
            return node, parent

    def rotate_left(self, node):
        """
        move the right red link of a node to the left
        initial status: node is BLACK, node.right is RED 
        this method used to rotate these two nodes counter-clockwise, and make the left child RED (right->BLACK)
        -> node.right move to node's original position, and the node will be the left child of node.right
        """
        t = node.right
        node.right = t.left
        t.left = node
        t.color = node.color
        node.color = RED
        return t 

    def rotate_right(self, node):
        """
        move the left red link of a node to the right
        opposite case of rotate_left(node)
        """
        t = node.left
        node.left = t.right
        t.right = node
        t.color = node.color
        node.color = RED
        return t

    def flip_colors(self, node):
        """
        if two links' color are the same, change both to the other color, 
        and make the parent's color reversed also
        """
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
        self.root.color = BLACK

    def _insert(self, node, key, value):
        """
        insert a new node(RED)
        case 0: right child is RED, left child is BLACK -> rotate_left
        case 1: left child is RED, left child's child is also RED -> rotate_right
        case 2: both two children are RED -> flip_colors
        """
        if node is None:
            return Node(key, value, RED)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        
        if (not self.is_red(node.left)) and self.is_red(node.right):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        return node

    def move_red_left(self, node):
        """
        make the red color node on the left side for deleting a node 
        case 0: node.left & node.left.left are all BLACK, node.right.left is also BLACK -> flip_colors
        case 1: node.left & node.left.left are all BLACK, and node.right.left is RED -> move RED to the left
        """
        self.flip_colors(node)
        if self.is_red(node.right.left):
            node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)
            self.flip_colors(node)
        return node

    def minimum_node(self, node):
        """get the minimum key node from the subtree"""
        if node.left is None:
            return node
        else:
            return self.minimum_node(node.left)

    def delete_min(self):
        """delete a node which has the min key"""
        self.root = self._delete_min(self.root)
        self.root.color = BLACK

    def _delete_min(self, node):
        if node.left is None:
            return None
        if (not self.is_red(node.left)) and (not self.is_red(node.left.left)):
            node = self.move_red_left(node)
        node.left = self._delete_min(node.left)
        return self.fix_up(node)
    
    def fix_up(self, node):
        """fix the structure of RBT after deleting a node"""
        if self.is_red(node.right):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)
        return node
    
    def delete_tmp(self, key):
        changing_node, parent = self._search_node(self.root, key)
        left_change = (parent.left == changing_node)
        if changing_node is None:
            raise KeyError(key)
        elif changing_node.right is None:
            if self.is_red(changing_node):
                if left_change:
                    parent.left = changing_node.left
                else:
                    parent.right = changing_node.left
            elif self.is_red(changing_node.left):
                changing_node.left.color = BLACK
                if left_change:
                    parent.left = changing_node.left
                else:
                    parent.right = changing_node.left
            else: # both black
                pass
                # ToDo
        else:
            min_node = self.minimum_node(changing_node.right)
            # copy node key, value
            changing_node.key = min_node.key
            changing_node.value = min_node.value
            changing_node.right = self._delete_min(changing_node.right)
        

if __name__ == '__main__':
    """test"""
    rbt = RedBlackTree()
    rbt.insert(12, 'A')
    rbt.insert(9, 'B')
    rbt.insert(15, 'C')
    rbt.insert(16, 'D')
    rbt.insert(18, 'E')

    print('after insertion')
    bst_utils.in_order(rbt.root)

    print('delete min')
    rbt.delete_min()

    bst_utils.in_order(rbt.root)
    print('abc', rbt.root.left.right)
