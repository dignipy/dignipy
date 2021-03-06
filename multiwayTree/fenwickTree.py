import collections


class FenwickTree(collections.abc.MutableSequence):
    """list implementation with prefix sum"""

    def __init__(self, iterable=[]):
        self.elements = lst = []
        for value in iterable:
            lst.append(value)
        self._fenwick_tree = [0]
        self._fill_tree_from(1)

    def __repr__(self):
        return 'FenwickTree({})'.format(repr(self.elements))

    def __str__(self):
        return 'FenwickTree({})'.format(str(self.elements))

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __delitem__(self, index):
        self.elements.__delitem__(index)
        tree_idx = index + 1
        self._fill_tree_from(tree_idx)

    def delete(self, index):
        self.__delitem__(index)

    def insert(self, index, value):
        self.elements.insert(index, value)
        tree_idx = index + 1
        self._fill_tree_from(tree_idx)

    def __setitem__(self, index, value):
        old_value = self.elements.__getitem__(index)
        self.elements.__setitem__(index, value)
        diff = value - old_value
        if diff == 0:
            return
        tree_idx = index + 1
        affected = self._affected_indices(tree_idx)
        for idx in affected:
            self._fenwick_tree[idx] += diff

    def __getitem__(self, index):
        return self.elements.__getitem__(index)

    def append(self, value):
        self.insert(len(self), value)

    def prefix_sum(self, list_idx):
        """get sum of elements upto list_idx"""
        tree_idx = list_idx + 1
        node_value = self._fenwick_tree[tree_idx]
        parent_idx = self._parent_index(tree_idx)
        if parent_idx == 0:
            parent_sum = 0
        else:
            parent_sum = self.prefix_sum(parent_idx - 1)
        return node_value + parent_sum

    def _parent_index(self, tree_idx):
        """get the parent's index in tree"""
        return tree_idx - (tree_idx & -tree_idx)

    def _children_indices(self, tree_idx):
        """get the list of children indices"""
        children = []
        if tree_idx == 0:
            max_idx = len(self.elements)
            idx = 1
            while idx <= max_idx:
                children.append(idx)
                idx *= 2
            return children

        diff = tree_idx & -tree_idx
        if diff == 0:
            return []
        while diff != 1:
            diff //= 2
            children.append(tree_idx + diff)
        return children
    
    def _children_indices_with_minimum(self, tree_idx, mini):
        """get the list of children indices"""
        children = []
        max_idx = len(self.elements)
        if tree_idx == 0:
            idx = 1
            while idx <= max_idx:
                if mini <= idx:
                    children.append(idx)
                idx *= 2
            return children

        diff = tree_idx & -tree_idx
        if diff == 0:
            return []
        while diff != 1:
            diff //= 2
            if tree_idx + diff > max_idx:
                continue
            elif tree_idx + diff < mini:
                break
            else:
                children.append(tree_idx + diff)
            
        return children
    
    def _affected_indices(self, tree_idx):
        
        p_list = []
        p_idx = self._parent_index(tree_idx)
        while p_idx > 0:
            p_list.append(p_idx)
            p_idx = self._parent_index(p_idx)
        p_list.append(0)
            
        affected = []
        for p_idx in p_list:
            candidates = self._children_indices_with_minimum(p_idx, tree_idx)
            affected.extend(candidates)
        return affected

    def bk_affected_indices(self, tree_idx):
        """get list of indices affected when changing elements[tree_idx-1]"""
        output = [tree_idx]
        max_tree_idx = len(self._fenwick_tree) - 1
        tmp_prefix = int(tree_idx) >> 2
        cur = 1
        while True:
            new_idx = tmp_prefix << (cur + 1) + 2**cur
            if tree_idx < new_idx <= max_tree_idx:
                output.append(new_idx)
            tmp_prefix >>= 1
            if tmp_prefix == 0:
                break
            cur += 1

        new_idx = 2**(cur + 1)
        while new_idx <= max_tree_idx:
            if new_idx > tree_idx:
                output.append(new_idx)
            new_idx <<= 1
        return output

    def _fill_tree_from(self, tree_idx):
        sum_start = tree_idx - 1
        sums = self._summation_from(sum_start)
        for idx in range(tree_idx, len(self.elements) + 1):
            sum_value = sums[idx - 1 - sum_start]
            parent_idx = self._parent_index(idx)
            if parent_idx == 0:
                parent_sum = 0
            elif parent_idx < tree_idx:
                list_idx = parent_idx - 1
                parent_sum = self.prefix_sum(list_idx)
            else:
                list_idx = parent_idx - 1
                parent_sum = sums[list_idx - sum_start]
            node_value = sum_value - parent_sum
            if len(self._fenwick_tree) == idx:
                self._fenwick_tree.append(node_value)
            else:
                self._fenwick_tree[idx] = node_value
        tree_len = len(self._fenwick_tree)
        target_len = len(self.elements) + 1
        if tree_len > target_len:
            num_delete = tree_len - target_len
            if num_delete <= tree_len:
                for _ in range(num_delete):
                    self._fenwick_tree.pop()
            else:
                self._fenwick_tree = self._fenwick_tree[:target_len]

    def _summation_from(self, list_idx):
        """helper function to make batch update"""
        if list_idx == 0:
            summation = 0
        else:
            summation = self.prefix_sum(list_idx - 1)
        sums = []
        for idx in range(list_idx, len(self.elements)):
            summation += self.elements[idx]
            sums.append(summation)
        return sums