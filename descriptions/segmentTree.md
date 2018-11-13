
# Segment Tree

>A segment tree also known as a statistic tree is a tree data structure used for storing information about intervals, or segments. It allows querying which of the stored segments contain a given point. It is, in principle, a static structure; that is, it's a structure that cannot be modified once it's built. 

>A segment tree for a set I of n intervals uses O(n log n) storage and can be built in O(n log n) time. Segment trees support searching for all the intervals that contain a query point in O(log n + k), k being the number of retrieved intervals or segments. - [Wikipedia](https://en.wikipedia.org/wiki/Segment_tree)



# Tree Structure
A segment tree is built from a given set `I` of intervals. The leaves are the sorted endpoints and the intervals in between. A [balanced](https://en.wikipedia.org/wiki/Binary_tree#Types_of_binary_trees) binary tree is built from the leaves.

A node in a segment tree represents an interval, which can have any combination of open or closed endpoints. Also, a subset of the given set `I` is assigned to each node. This `canonical subset` contains the intervals from `I` that contains the interval of the node, but does not contain the interval of the parent node. Thus, viewed from the top, an interval `intv` from `I` relates to the first nodes that are contained in `intv`.

# Querying
`Under construction`
