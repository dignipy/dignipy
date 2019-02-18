'''ahocorasick.py

This module implements Aho-corasick Trie

Aho-corasick Trie
- can find patterns {A, B, C...} in Text efficiently
    - if n: length of text, m: length of each patterns
    - Brute-force method takes O(n * (m1 + m2 + m3 + ... + mk))
    - But, Aho-corasick takes O(n + m1 + m2 + ... mk)

Each nodes have
- go-links (it contains children, also called go function)
- a failure-link(also called failure function)
- an output-link(also called output function)

Related Problem:
- https://www.acmicpc.net/problem/9250
'''
import collections

class AhoCorasickTrie():
    _cnt = 0
    _root = None
    
    def __init__(self, key=None):
        AhoCorasickTrie._cnt += 1
        self._id = AhoCorasickTrie._cnt # for debugging
        self.key = key
        self.go = {}
        self.fail = None
        self.output = None
        self.pattern = None
    
    def __repr__(self):
        fail_id = self.fail._id if self.fail else '@'
        output_id = self.output._id if self.output else '@'
        return '[#{}]Node({}, {}, {}-{})'.format(self._id, self.key, fail_id, output_id, self.pattern)

    @classmethod
    def _insert_word_from(cls, word):
        cur_node = cls._root
        for key in word:
            if key not in cur_node.go:
                new_node = AhoCorasickTrie(key)
                cur_node.go[key] = new_node
                cur_node = new_node
            else:
                cur_node = cur_node.go[key]
        cur_node.output = cur_node
        cur_node.pattern = word
    
    @classmethod
    def _set_failure_links(cls):
        Q = collections.deque() # for BFS
        cls._root.fail = cls._root;
        Q.append(cls._root)
        while Q:
            # check 'current', 'next' node then set the failure, output link of child nodes
            current = Q.popleft()
            for _, child_node in current.go.items():
                next = child_node
                if current == cls._root:
                    next.fail = cls._root
                else:
                    dest = current.fail
                    # go upward to find node which has next.key in its go link
                    while dest != cls._root and not (next.key in dest.go):
                        dest = dest.fail
                    if next.key in dest.go:
                        dest = dest.go[next.key]
                    next.fail = dest
                # fail(x) = y, output(y) ⊂ output(x)
                if next.fail.output:
                    next.output = next.fail.output
                Q.append(next)
        # End of while Q
        
    @classmethod
    def _show_all_by_dfs(cls, node, level=0, msg=''):
        if level == 0:
            print('--------------------------------------')
            print(msg)
            print('--------------------------------------')
        print((' ' * 2 * level) + str(node))
        for _, child_node in node.go.items():
            cls._show_all_by_dfs(child_node, level + 1)
            
    @classmethod
    def build_from(cls, patterns, debug=False):
        cls._root = AhoCorasickTrie()
        for pattern in patterns:
            cls._insert_word_from(pattern)
        if debug: cls._show_all_by_dfs(cls._root, msg='Before Setting Failure Links')
        cls._set_failure_links()
        if debug: cls._show_all_by_dfs(cls._root, msg='After Setting Failure Links')
        
    @classmethod
    def search_patterns_in(cls, text):
        patterns = set()
        current = cls._root
        for next_char in text:
            while current != cls._root and not (next_char in current.go):
                current = current.fail
            if next_char in current.go:
                current = current.go[next_char]
            if current.output:
                tmp = current
                while tmp and tmp.output:
                    if tmp.pattern: patterns.add(tmp.pattern)
                    if tmp == tmp.output: break
                    tmp = tmp.output
        return patterns
    
    
if __name__ == '__main__':
    #patterns = ['a', 'ab', 'ac', 'adab', 'adada', 'adac', 'd']
    #patterns = ['a', 'ab', 'c', 'acd']
    #patterns = ['abcd', 'ad']
    #patterns = ['bcab', 'bcada', 'a']
    patterns = ['his', 'he', 'she', 'hers']
    
    AhoCorasickTrie.build_from(patterns, debug=True)
    
    #print(AhoCorasickTrie.search_patterns_in('adacab'))
    #print(AhoCorasickTrie.search_patterns_in('acadab'))
    print(AhoCorasickTrie.search_patterns_in('she'))
    print(AhoCorasickTrie.search_patterns_in('hershe'))
