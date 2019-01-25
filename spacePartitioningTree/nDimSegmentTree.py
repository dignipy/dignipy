# -*- coding: utf-8 -*-
"""nDimSegmentTree.py

This module implements multi dimensional segment tree.

A segment tree also known as a statistic tree is a tree data structure used
for storing information about intervals, or segments. It allows querying
which of the stored segments contain a given point. It is, in principle, a
static structure; that is, it's a structure that cannot be modified once it's
built.

A segment tree for a set I of n intervals uses O(n log n) storage and can be
built in O(n log n) time. Segment trees support searching for all the intervals
that contain a query point in O(log n + k), k being the number of retrieved
intervals or segments.

For multi dimensional implementation, there are some modifications to some of
the object like axis index. However 1-dim segment tree is still available, and
segmentTree.py is redundant.

"""

import math


class Interval():
    def __init__(self, left_endpoint, right_endpoint, l_closed, r_closed):
        self.left_endpoint = left_endpoint  # float or int
        self.right_endpoint = right_endpoint  # float or int
        self.left_closed = l_closed  # bool, whether left enpoint is closed
        self.right_closed = r_closed  # bool, whether right enpoint is closed
        self.cube = None  # the cube which this interval belongs as a side
        self.axis = None

    def __repr__(self):
        """ mathematical representation of an interval """
        s = "{}, {}".format(self.left_endpoint, self.right_endpoint)
        if self.left_closed:
            left_bracket = '['
        else:
            left_bracket = '('

        if self.right_closed:
            right_bracket = ']'
        else:
            right_bracket = ')'
        interval_string = left_bracket + s + right_bracket
        return 'Interval({})'.format(interval_string)

    def contains(self, another_interval):
        """ check if this interval contains another_interval """
        if another_interval.left_endpoint < self.left_endpoint:
            return False
        if another_interval.left_endpoint == self.left_endpoint:
            if not self.left_closed and another_interval.left_closed:
                return False
        if another_interval.right_endpoint > self.right_endpoint:
            return False
        if another_interval.right_endpoint == self.right_endpoint:
            if not self.right_closed and another_interval.right_closed:
                return False
        return True

    def intersects(self, interval):
        raise NotImplementedError('To do: implement intersection check')


class Cube():
    """ n-dimensional cube which is a product of intervals"""
    def __init__(self, sides):
        self.dimension = len(sides)
        self.sides = sides
        for axis, interval in enumerate(sides):
            interval.cube = self
            interval.axis = axis
    
    def __repr__(self):
        return 'Cube'+repr(tuple(self.sides))
    

class TreeNode():
    def __init__(self, left_endpoint, right_endpoint, l_closed, r_closed):
        self.left = None
        self.right = None
        intv = Interval(left_endpoint, right_endpoint, l_closed, r_closed)
        self.interval = intv
        self.left_endpoint = left_endpoint
        self.right_endpoint = right_endpoint
        self.left_closed = l_closed
        self.right_closed = r_closed
        self.subset = []  # the canonical subset of given intervals

        self.axis = None # axis this tree belongs to
        self.next_axis_tree = None  # sub segment tree for this node in next axis

    def __repr__(self):
        """ mathematical representation of the node's interval """
        s = "{}, {}".format(self.left_endpoint, self.right_endpoint)
        if self.left_closed:
            left_bracket = '['
        else:
            left_bracket = '('

        if self.right_closed:
            right_bracket = ']'
        else:
            right_bracket = ')'
        interval_string = left_bracket + s + right_bracket
        return 'TreeNode({})'.format(interval_string)

    def query(self, point):
        """ return list of Interval objects containing point in the subtree """
        point_interval = Interval(point, point, True, True)
        # point is also a closed interval [p, p]

        if not self.interval.contains(point_interval):
            # this node's interval doesn't contain point
            return []

        found = []
        for intv in self.subset:
            found.append(intv)
            # because intv contains the node's interval, which contains point
        if self.left is not None:
            for intv in self.left.query(point):
                found.append(intv)
        if self.right is not None:
            for intv in self.right.query(point):
                found.append(intv)
        return found

    def path_to_leaf(self, point, prev_path=None):
        point_interval = Interval(point, point, True, True)

        if prev_path is None:
            prev_path = [self]
        else:
            prev_path.append(self)

        if self.left is not None:
            if self.left.interval.contains(point_interval):
                return self.left.path_to_leaf(point, prev_path=prev_path)
        if self.right is not None:
            if self.right.interval.contains(point_interval):
                return self.right.path_to_leaf(point, prev_path=prev_path)
            else:
                return []
        else:
            return prev_path


class SegmentTree():
    def __init__(self, intervals):
        self.intervals = intervals
        self.root = None
        self.build_tree()

    def query(self, point):
        """ return list of all Interval objects containing point """
        if self.root is None:
            raise Exception('tree must be built first')
        return self.root.query(point)
    
    def root_to_leaf(self, point):
        return self.root.path_to_leaf(point)

    def build_tree(self):
        """ Build segment tree from given intervals and return the root.
            Takes O(n log(n)) time.
        """
        intervals = self.intervals

        # sort all endpoints and make intervals for leaf nodes
        endpoints = []
        for interval in intervals:
            endpoints.append(interval.left_endpoint)
            endpoints.append(interval.right_endpoint)
        endpoints.append(float('inf'))
        endpoints.append(float('-inf'))

        endpoints.sort()
        unique_endpoints = []
        for i, ep in enumerate(endpoints):
            if i + 1 < len(endpoints) and ep == endpoints[i + 1]:
                continue
            else:
                unique_endpoints.append(ep)


        # append tuples for making intervals:
        # (left_endpoint, right_endpoint, l_closed, r_closed)
        # if left_enpoint == right_endpoint: it represents a point
        endpoints = unique_endpoints
        elements = []
        for i, ep in enumerate(endpoints):
            if i == 0:
                prev = ep
                continue
            elif i < len(endpoints) - 1:
                elements.append((prev, ep, False, False))
                elements.append((ep, ep, True, True))
                prev = ep
            else:  # i == len(endpoints)-1
                elements.append((prev, ep, False, False))

        num_leaves = len(elements)

        max_depth = int(math.log(num_leaves) / math.log(2)) + 1
        num_last_leaves = 2 * (num_leaves - 2**(max_depth - 1))

        # build tree from bottom to up

        # make a queue for each depth
        q = []
        for i, elem in enumerate(elements):
            if i < num_last_leaves:
                if i % 2 == 0:
                    prev = elem
                else:
                    left_node = TreeNode(*prev)
                    right_node = TreeNode(*elem)
                    node = TreeNode(prev[0], elem[1], prev[2], elem[3])
                    node.left = left_node
                    node.right = right_node
                    q.append(node)
            else:
                node = TreeNode(*elem)
                q.append(node)

        # while depth > 0
        while len(q) > 1:
            tmp_q = []
            for i, node in enumerate(q):
                if i % 2 == 0:
                    prev = node
                else:
                    left_ep = prev.left_endpoint
                    right_ep = node.right_endpoint
                    l_closed = prev.left_closed
                    r_closed = node.right_closed
                    new_node = TreeNode(left_ep, right_ep, l_closed, r_closed)
                    new_node.left = prev
                    new_node.right = node
                    tmp_q.append(new_node)
            q = tmp_q

        self.root = q[0]

        # add canonical subsets
        for interval in intervals:
            self._append_subset(self.root, interval)

        return self.root

    def _append_subset(self, node, interval):
        """Recursive function to add canonical subsets"""
        if interval.contains(node.interval):
            node.subset.append(interval)
            return None
        if node.left is not None:
            self._append_subset(node.left, interval)
        if node.right is not None:
            self._append_subset(node.right, interval)
    
    def traverse(self, node, function):
        function(node)
        if node.left is not None:
            self.traverse(node.left, function)
        if node.right is not None:
            self.traverse(node.right, function)


if __name__ == '__main__':
    import random
    intervals = []
    for _ in range(10):
        endpoints = []
        endpoints.append(random.choice(list(range(100))))
        endpoints.append(random.choice(list(range(100))))
        l_closed = random.choice([False, True])
        r_closed = random.choice([False, True])
        intv = Interval(min(endpoints), max(endpoints), l_closed, r_closed)
        intervals.append(intv)
    print('intervals:', intervals)
    seg_tree = SegmentTree(intervals)
    print('intervals containing 34:', seg_tree.query(34))

    rectangles = []
    for _ in range(3):
        rect = []
        for _ in range(2):
            endpoints = []
            endpoints.append(random.choice(list(range(100))))
            endpoints.append(random.choice(list(range(100))))
            l_closed = random.choice([False, True])
            r_closed = random.choice([False, True])
            intv = Interval(min(endpoints), max(endpoints), l_closed, r_closed)
            rect.append(intv)
        rectangles.append(Cube(rect))

    def attach_seg_tree(node):
        """ attach a new segment tree to every TreeNode of the segment tree in dim 0 """
        axis = 0
        node.axis = axis
        cannonical_subset = node.subset
        cubes = [intv.cube for intv in cannonical_subset]
        intervals = [c.sides[axis] for c in cubes]
        node.next_axis_tree = SegmentTree(intervals)

    dim = 0
    seg_tree_0 = SegmentTree([c.sides[dim] for c in rectangles])
    seg_tree_0.traverse(seg_tree_0.root, attach_seg_tree)
    
    print(rectangles)
    print('querying (40, 50)...')
    x = 40
    y = 50
    intervals0 = seg_tree_0.query(x)
    print('intervals in axis=0 containing x=40', intervals0)
    
    selected_cubes = []
    path = seg_tree_0.root_to_leaf(x)
    for node in path:
        sub_seg_tree = node.next_axis_tree
        intervals1 = sub_seg_tree.query(y)
        for intv in intervals1:
            c = intv.cube
            selected_cubes.append(c)
    print('found cubes', selected_cubes)