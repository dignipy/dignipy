"""bst_utils.py

This module implements common methods for visiting Binary Search Tree's nodes 

"""


def in_order(node, function=None):
    if node is None:
        return 
    in_order(node.left, function=function)
    if not function:
        print(node)
    else:
        function(node)
    in_order(node.right, function=function)

def pre_order(node, function=None):
    if node is None:
        return 
    if not function:
        print(node)
    else:
        function(node)
    in_order(node.left, function=function)
    in_order(node.right, function=function)

def post_order(node, function=None):
    if node is None:
        return 
    in_order(node.left, function=function)
    in_order(node.right, function=function)
    if not function:
        print(node)
    else:
        function(node)

def print_tree(root_node):
    try:
        import anytree
        TreeNode = anytree.Node
        key2tree = dict()
        key2tree[root_node.key] = TreeNode(repr(root_node))
        def add_parent(child, parent):
            key2tree[child.key] = TreeNode(repr(child), parent=key2tree[parent.key])

        def connect(node):
            if node.left is not None:
                add_parent(node.left, node)
            if node.right is not None:
                add_parent(node.right, node)
        pre_order(root_node, function=connect)
        render = anytree.RenderTree(key2tree[root_node.key])
        for pre, _, node in render:
            print("%s%s" % (pre, node.name))
    except Exception as e:
        print(repr(e))