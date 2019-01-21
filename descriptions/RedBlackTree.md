# Red-Black Tree

> A Red-Black tree is a kind of self-balancing search tree. Each node of the binary tree has an extra bit, and that bit is often interpreted as the color(red or black) of the node. These color bits are used to ensure the tree remains approximately balanced during insertions and deletions. - [Wikipedia](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)

- Reb-Black tree use color(red, black) to balance itself
- Searching, Inserting, Deleting time < O(logN)

# Left-Leaning Red-Black tree(LLRB)
> We have to consider too many cases to implements Vanilla Red-Black tree's insertion, deletion operations. But, Left-Learning Red-Black tree(a variant of the RBT) is much simpler than the original. The number of lines of code maybe 1/5 of vanilla red-black tree. It is even more efficient than AVL-tree, 2-3-tree, 2-3-4-tree, and the general red-black trees.


# Properties(Invariants)
- Each node is either RED or BLACK
- The root and null(leaf) are BLACK
- There are **no two consecutive RED** nodes.
  - if a node is RED, then its children are BLACK
- All of the RED links are **left-leaning**
- Every paths from the root to the leaves contain **the same number of black nodes**


# Methods

## insert(key, value)
- runs in O(log n) time

## delete_min()
- runs in O(log n) time

## delete(key)
- runs in O(log n) time
