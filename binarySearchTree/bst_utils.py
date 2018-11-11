"""bst_utils.py

This module implements common methods for visiting Binary Search Tree's nodes 

"""


def in_order(node):
    if node is None:
        return 
    in_order(node.left)
    print(node)
    in_order(node.right)

def pre_order(node):
    if node is None:
        return 
    print(node)
    in_order(node.left)
    in_order(node.right)

def post_order(node):
    if node is None:
        return 
    in_order(node.left)
    in_order(node.right)
    print(node)

