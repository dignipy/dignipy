""" nQueens.ipynb

This module implements the solution for N queens puzzle.

The N queens puzzle is the problem of placing N chess queens on an N x N
chessboard so that no two queens threaten each other. Thus, a solution requires
that no two queens share the same row, column, or diagonal.

The solution uses Zero-suppressed decision diagrams as in
'Zero-suppressed BDDs and their applications, Minato, 2001'

"""

import context  # adds submodules to sys.path

from graph import ZDD


def avoid_positions(pos, n):
    """ returns the list of positions to avoid
        when placing a queen on pos upto row pos[0] - 1
    """
    avoid = []
    (row, col) = pos
    row -= 1
    col_left = col - 1
    col_right = col + 1
    while row >= 0:
        if 0 <= col_left < n:
            avoid.append((row, col_left))
        if 0 <= col_right < n:
            avoid.append((row, col_right))
        avoid.append((row, col))
        row -= 1
        col_left -= 1
        col_right += 1
    return avoid


def chain(func, args):
    """ chains the func along args """
    x = args[0]
    for y in args[1:]:
        x = func(x, y)
    return x


def n_queens(n):
    """ N queens solver """
    zdd = ZDD.ZDD()
    position2node = dict()
    empty = zdd.empty()
    base = zdd.base()

    # assign n**2 elementary nodes
    idx = 0
    for i in range(n):
        for j in range(n):
            x = zdd.get_node(idx, empty, base)
            position2node[(i, j)] = x
            idx += 1

    # s_dict[i] is the zdd of N queens upto row i
    args = [position2node[(0, j)] for j in range(n)]
    s0 = chain(zdd.union, args)

    s_dict = dict()
    s_dict[0] = s0

    for i in range(1, n):
        union_list = []
        for j in range(n):
            avoid = avoid_positions((i, j), n)
            args = [s_dict[i - 1]] + [position2node[y] for y in avoid]
            tmp = chain(zdd.remainder, args)
            # from s_dict[i-1], remove cases to avoid when placing x
            # it might be faster with offset method instead of remainder

            x = position2node[(i, j)]
            # multiply x to the cube (place x at position (i, j))
            prod = zdd.product(x, tmp)
            union_list.append(prod)
        # union of all the placement in row i
        s_dict[i] = chain(zdd.union, union_list)

    return zdd.count(s_dict[n - 1])

import time
print(time.time())
print('n_queens(1)=', n_queens(1))
print(time.time())
print('n_queens(2)=', n_queens(2))
print(time.time())
print('n_queens(3)=', n_queens(3))
print(time.time())
print('n_queens(4)=', n_queens(4))
print(time.time())
print('n_queens(5)=', n_queens(5))
print(time.time())
print('n_queens(6)=', n_queens(6))
print(time.time())
print('n_queens(7)=', n_queens(7))
print(time.time())
print('n_queens(8)=', n_queens(8))
print(time.time())
print('n_queens(9)=', n_queens(9))
print(time.time())
print('n_queens(15)=', n_queens(15))
print(time.time())

