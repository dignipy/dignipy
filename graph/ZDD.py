# coding: utf-8

import weakref


class Node():
    def __init__(self, top, key=None, lo=None, hi=None):
        """
        top: nonnegative integer except for terminal nodes
        key: unique key to identify the node
        lo: the node that the 0-edge leads to
        hi: the node that the 1-edge leads to
        """
        self.top = top
        self.lo = lo
        self.hi = hi
        self._unique_key = key
        # self._parent = None

    def __repr__(self):
        format_info = [self.top, self._unique_key, self.lo, self.hi]
        return 'Node({}, key={}, lo={}, hi={})'.format(*format_info)


class ZDD():
    def __init__(self):
        # garbage collect removed nodes
        self._unique_table = weakref.WeakValueDictionary()

        # self.level2nodes = collections.defaultdict(list)
        self._base = None
        self._empty = None
        self._next_unique_key = 0

    def get_node(self, top, p0, p1):
        """ function to take care of all node creation and access """
        if p0 is True and p1 is True:
            key0 = key1 = True
        elif p0 is False and p1 is False:
            key0 = key1 = False
        else:
            key0 = p0._unique_key
            key1 = p1._unique_key

        if p1 is self.empty():
            return p0
        elif (top, key0, key1) in self._unique_table:
            return self._unique_table[(top, key0, key1)]
        else:
            p = Node(top, key=self._next_unique_key, lo=p0, hi=p1)
            self._unique_table[(top, key0, key1)] = p
            self._next_unique_key += 1
            return p

    def empty(self):
        """ returns ⊥ terminal node """
        # top = -1
        if self._empty is None:
            key = self._next_unique_key
            self._next_unique_key += 1
            self._empty = Node(-1, key=key, lo=False, hi=False)
            self._unique_table[(-1, False, False)] = self._empty
        return self._empty

    def base(self):
        """ returns ⊤ terminal node """
        # top = -1
        if self._base is None:
            key = self._next_unique_key
            self._next_unique_key += 1
            self._base = Node(-1, key=key, lo=True, hi=True)
            self._unique_table[(-1, True, True)] = self._base
        return self._base

    def offset(self, p, var):
        """ returns the top node of ZDD when var is 0 with var node removed """
        empty = self.empty()
        base = self.base()
        if p is empty:
            return empty
        elif p is base:
            return base
        elif p.top < var:
            return p
        elif p.top == var:
            return p.lo
        else:
            lo_subset = self.offset(p.lo, var)
            hi_subset = self.offset(p.hi, var)
            return self.get_node(p.top, lo_subset, hi_subset)

    def onset(self, p, var):
        """ returns the top node of ZDD when var is 1 with var node removed """
        empty = self.empty()
        base = self.base()
        if p is empty:
            return empty
        elif p is base:
            return empty
        elif p.top < var:
            return empty
        elif p.top == var:
            return p.hi
        else:
            lo_subset = self.onset(p.lo, var)
            hi_subset = self.onset(p.hi, var)
            return self.get_node(p.top, lo_subset, hi_subset)

    def change(self, p, var):
        """ change hi and lo edges of the var node """
        if p.top < var:
            empty = self.empty()
            return self.get_node(var, empty, p)
        elif p.top == var:
            return self.get_node(var, p.hi, p.lo)
        else:
            lo_change = self.change(p.lo, var)
            hi_change = self.change(p.hi, var)
            return self.get_node(p.top, lo_change, hi_change)

    def union(self, p, q):
        """ union of 1-paths"""
        empty = self.empty()
        if p == empty:
            return q
        elif q == empty:
            return p
        elif p == q:
            return p
        elif p.top > q.top:
            return self.get_node(p.top, self.union(p.lo, q), p.hi)
        elif p.top < q.top:
            return self.get_node(q.top, self.union(p, q.lo), q.hi)
        else:
            lo_union = self.union(p.lo, q.lo)
            hi_union = self.union(p.hi, q.hi)
            return self.get_node(p.top, lo_union, hi_union)

    def intersection(self, p, q):
        """ intersetction of 1-paths """
        empty = self.empty()
        if p == empty:
            return empty
        elif q == empty:
            return empty
        elif p == q:
            return p
        elif p.top > q.top:
            return self.intersection(p.lo, q)
        elif p.top < q.top:
            return self.intersection(p, q.lo)
        else:
            lo_intersect = self.intersection(p.lo, q.lo)
            hi_intersect = self.intersection(p.hi, q.hi)
            return self.get_node(p.top, lo_intersect, hi_intersect)

    def difference(self, p, q):
        """ set difference of 1-paths """
        empty = self.empty()
        if p == empty:
            return empty
        elif q == empty:
            return p
        elif p == q:
            return empty
        elif p.top > q.top:
            return self.get_node(p.top, self.difference(p.lo, q), p.hi)
        elif p.top < q.top:
            return self.difference(p, q.lo)
        else:
            lo_diff = self.difference(p.lo, q.lo)
            hi_diff = self.difference(p.hi, q.hi)
            return self.get_node(p.top, lo_diff, hi_diff)

    def count(self, p):
        """ count the number of 1-paths """
        if p is self.empty():
            return 0
        elif p is self.base():
            return 1
        else:
            return self.count(p.lo) + self.count(p.hi)

    def get_set(self, p):
        """ change ZDD to a corresponding family of sets """
        if p is self.empty():
            return frozenset([])  # use frozenset for hashing
        elif p is self.base():
            return frozenset([frozenset([])])
        f1 = self.get_set(p.hi)
        top_set = set([p.top])
        f1_with_top = [frozenset([s.union(top_set)]) for s in f1]
        return frozenset.union(self.get_set(p.lo), *f1_with_top)

    def product(self, p, q):
        """ return the family of all possible concatenations of
            any two respective cubes in p and q
        """
        empty = self.empty()
        base = self.base()
        if p is empty:
            return empty
        elif p is base:
            return q
        elif q is empty:
            return empty
        elif q is base:
            return p
        elif p.top < q.top:
            return self.product(q, p)
        else:
            var = p.top
            p0 = self.offset(p, var)
            p1 = self.onset(p, var)
            q0 = self.offset(q, var)
            q1 = self.onset(q, var)
            r0 = self.product(p0, q0)
            tmp1 = self.product(p1, q1)
            tmp2 = self.union(tmp1, self.product(p1, q0))
            r1 = self.union(tmp2, self.product(p0, q1))
            return self.get_node(var, r0, r1)

    def division(self, p, q):
        """ when q includes only one cube, p/q is obtained by extracting
            a subset of P, which consists of the cubes including all the
            literals in q's cube, when q consists of multiple cubes,
            p/q is the intersection of all the quotients dividing p by
            respective cubes in q
        """
        empty = self.empty()
        base = self.base()
        if q is base:
            return p
        elif p is empty or p is base:
            return empty
        elif p is q:
            return base
        else:
            var = q.top
            p0 = self.offset(p, var)
            p1 = self.onset(p, var)
            q0 = self.offset(q, var)
            q1 = self.onset(q, var)
            result = self.division(p1, q1)
            if result is not empty and q0 is not empty:
                div = self.division(p0, q0)
                result = self.intersection(result, div)
            return result

    def remainder(self, p, q):
        """ calculate p - (q * (p/q)) """
        div = self.division(p, q)
        prod = self.product(q, div)
        return self.difference(p, prod)

    def is_excluded(self, p, var):
        if p.top < var:
            return True
        elif p.top == var:
            return False
        else:
            lo_excluded = self.is_excluded(p.lo, var)
            hi_excluded = self.is_excluded(p.hi, var)
            return lo_excluded and hi_excluded

    def make_free(self, p, var):
        """
        make the var node free (no restriction condition on var)
        """
        if p.top < var:
            return self.get_node(var, p, p)
        elif p.top == var:
            tmp_p = self.change(p, var)
            return self.union(p, tmp_p)
        else:
            # p.top > var
            new_lo = self.make_free(p.lo, var)
            new_hi = self.make_free(p.hi, var)
            return self.get_node(p.top, new_lo, new_hi)

    def from_set(self, in_set):
        """ return the top node of the correstponding ZDD of in_set """
        if in_set == frozenset():
            return self.empty()
        elif in_set == frozenset([frozenset()]):
            return self.base()
        max_var = self._get_max_var(in_set)
        onset = set()
        offset = set()
        var_set = set([max_var])
        for cube_set in in_set:
            if max_var in cube_set:
                onset.add(cube_set - var_set)
            else:
                offset.add(cube_set)
        p0 = self.from_set(offset)
        p1 = self.from_set(onset)
        return self.get_node(max_var, p0, p1)

    def _get_max_var(self, in_set):
        """ get max variable from all the sets in the in_set family """
        tmp_max = float('-inf')
        for cube_set in in_set:
            if len(cube_set) == 0:
                continue
            tmp_max = max(tmp_max, max(cube_set))
        if tmp_max < 0:
            raise ValueError('Not a supported set type')
        return tmp_max


if __name__ == '__main__':
    zdd = ZDD()

    base = zdd.base()
    empty = zdd.empty()

    a = zdd.get_node(1, empty, base)
    print('a: identity function,', zdd.get_set(a))
    b = zdd.get_node(2, empty, a)
    print('b:', zdd.get_set(b))
    c = zdd.get_node(3, a, b)
    print('c:', zdd.get_set(c))
    print('b union c:', zdd.get_set(zdd.union(b, c)))
    print('b - c:', zdd.get_set(zdd.difference(b, c)))

    d_set = frozenset([frozenset([1, 2, 3]), frozenset([4])])
    d = zdd.from_set(d_set)
    print('d:', zdd.get_set(d))

    e_set = frozenset([frozenset([3])])
    e = zdd.from_set(e_set)
    print('e:', zdd.get_set(e))

    print('d * e: ', zdd.get_set(zdd.product(d, e)))
    print('d / e: ', zdd.get_set(zdd.division(d, e)))
