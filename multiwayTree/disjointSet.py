
class Node():
    def __init__(self, key=None):
        self.key = key
        self.parent = self
        self.size = 1  # size of tree


class DisjointSet():
    def __init__(self, key_list):
        self._key2node = dict()
        for key in key_list:
            if key in self._key2node:
                continue
            node = Node(key)
            self._key2node[key] = node

    def union(self, key1, key2):
        """ merge the two sets containing key1 and key2 """
        node1 = self._key2node[key1]
        node2 = self._key2node[key2]
        self.merge_root(node1, node2)

    def find(self, node):
        """find the root node from the input node"""
        root, _ = self._get_upward_path(node)
        return root

    def is_connected(self, key1, key2):
        """ returns whether two keys are in the same set or not """
        node1 = self._key2node[key1]
        node2 = self._key2node[key2]
        return self.is_connected_nodes(node1, node2)

    def is_connected_nodes(self, node1, node2):
        """ returns whether two nodes are in the same set or not """
        root1, upward_path1 = self._get_upward_path(node1)
        self._change_parent(root1, upward_path1)

        root2, upward_path2 = self._get_upward_path(node2)
        self._change_parent(root2, upward_path2)

        if root1 == root2:
            return True
        else:
            return False

    def merge_root(self, node1, node2):
        """
        Merge the sets containing node1 and node2
        attaching the smaller sized set's root to the larger
        """

        root1, upward_path1 = self._get_upward_path(node1)
        root2, upward_path2 = self._get_upward_path(node2)

        if root1 != root2:
            new_size = root1.size + root2.size
            if root1.size >= root2.size:
                root = root1
                root.size = new_size
                root2.size = None
                root2.parent = root
            else:
                root = root2
                root.size = new_size
                root1.size = None
                root1.parent = root
        else:
            root = root1

        # path compression
        self._change_parent(root, upward_path1)
        self._change_parent(root, upward_path2)

    def _get_upward_path(self, node):
        """get root node and the path to the root from the input node"""
        upward_path = []
        while True:
            p = node.parent
            if p == node:
                break
            upward_path.append(node)
            node = p
        root = node
        return root, upward_path

    def _change_parent(self, new_root, upward_path):
        """helper function to change parent of all nodes in a list"""
        for node in upward_path:
            node.parent = new_root


if __name__ == '__main__':
    num_keys = 100000
    key_list = list(range(num_keys))
    graph = DisjointSet(key_list)
    import random
    for _ in range(100000):
        edge = random.sample(key_list, 2)
        graph.union(*edge)

    answer = graph.is_connected(7, 9)
    print('Connected?', answer)
