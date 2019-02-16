'''ahocorasick.py

This module implements Aho-corasick Trie

Aho-corasick Trie
- can find patterns {A, B, C...} in Text efficiently
    - if n: length of text, m: length of each patterns
    - Brute-force method takes O(n * (m1 + m2 + m3 + ... + mk))
    - But, Aho-corasick takes O(n + m1 + m2 + ... mk)

Each nodes have
- go-links (it contains children)
- a failure-link(also called failure function)
- an output-link(also called output function)

Related Problem:
- https://www.acmicpc.net/problem/9250
'''
import collections

class AhoCorasickTrie():
    cnt = 0
    def __init__(self, key=None):
        AhoCorasickTrie.cnt += 1
        self.id = AhoCorasickTrie.cnt # for debugging
        self.key = key
        self.go = {}
        self.fail = None
        self.output = None
        self.pattern = None
    
    def __repr__(self):
        fail_id = self.fail.id if self.fail else '@'
        output_id = self.output.id if self.output else '@'
        return '[#{}]Node({}, {}, {}-{})'.format(self.id, self.key, fail_id, output_id, self.pattern)

    @classmethod
    def insert_word_from(cls, root, word):
        cur_node = root
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
    def set_failure_links(cls, root):
        Q = collections.deque() # for BFS
        root.fail = root;
        Q.append(root)
        while Q:
            # check 'current', 'next' node then set the failure, output link of child nodes
            current = Q.popleft()
            for _, child_node in current.go.items():
                next = child_node
                if current == root:
                    next.fail = root
                else:
                    dest = current.fail
                    # go upward to find node which has next.key in its go link
                    while dest != root and not (next.key in dest.go):
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
    def search(cls, root, text):
        patterns = set()
        current = root
        for next_char in text:
            while current != root and not (next_char in current.go):
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
    
    @classmethod
    def show_all_by_dfs(cls, node, level=0, msg=''):
        if level == 0:
            print(msg)
            print('--------------------------------------')
        print((' ' * 2 * level) + str(node))
        for _, child_node in node.go.items():
            cls.show_all_by_dfs(child_node, level + 1)
    
    
if __name__ == '__main__':
    patterns = ['a', 'ab', 'ac', 'adab', 'adada', 'adac']
    #patterns = ['a', 'ab', 'c', 'acd']
    #patterns = ['abcd', 'ad']
    #patterns = ['bcab', 'bcada', 'a']
    #patterns = ['his', 'he', 'she', 'hers']
    root = AhoCorasickTrie()
    for pattern in patterns:
        AhoCorasickTrie.insert_word_from(root, pattern)
    
    AhoCorasickTrie.show_all_by_dfs(root, msg='Before Setting Failure Links')
    
    AhoCorasickTrie.set_failure_links(root) # [TODO] 통합시키기
    AhoCorasickTrie.show_all_by_dfs(root, msg='After Setting Failure Links')
    
    print(AhoCorasickTrie.search(root, 'adacab'))
    #print(AhoCorasickTrie.search(root, 'she'))