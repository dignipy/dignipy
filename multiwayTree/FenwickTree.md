
# Fenwick Tree

>A Fenwick tree or binary indexed tree is a data structure that can efficiently update elements and calculate [prefix sums](https://en.wikipedia.org/wiki/Prefix_sum) in a table of numbers. This structure was proposed by Peter Fenwick in 1994 to improve the efficiency of arithmetic coding compression algorithms. - [Wikipedia](https://en.wikipedia.org/wiki/Fenwick_tree)

# Tree Structure
A node in a Fenwick tree has an index and a value. The root's index is 0 and the value is 0. A node's parent is found by clearing the least-significant bit in the index. Given (1-based) sequence, the value of a node is the sum of numbers since the parent's index in the tree. For example, the list `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]` can be drawn as follows.

![Fenwick Tree](./FenwickTreeImage.png)

# Methods

## prefix_sum( )
- runs in O(log n) time

## append( )
- runs in O(log n) time

## insert( )
- runs in O(n) time

## delete( )
- runs in O(n) time


