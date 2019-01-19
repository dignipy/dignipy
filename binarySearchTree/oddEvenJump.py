"""oddEvenJump.py

This module solves Odd Even Jumps problem:
https://leetcode.com/problems/odd-even-jump/

Uses Left-Leaning Red-Black Tree (LLRB)
Takes O(n log(n)) time

"""

import random
import time

import redBlackTree
        

class OddEvenJump():
    def __init__(self, A):
        rbt = redBlackTree.RedBlackTree()

        odd_jump = [-1]*len(A)
        even_jump = [-1]*len(A)

        for i in range(len(A)):
            idx = len(A) - 1 - i
            key = A[idx]
            searched = rbt.search(key)
            if searched is None:
                # no same key
                greater = rbt.search_greater_near(key)
                if greater is None:
                    # nowhere to odd-jump
                    odd_jump[idx] = idx
                else:
                    odd_jump[idx] = greater.value

                less = rbt.search_less_near(key)
                if less is None:
                    # nowhere to even-jump
                    even_jump[idx] = idx
                else:
                    even_jump[idx] = less.value

            else:
                # found same key
                odd_jump[idx] = searched
                even_jump[idx] = searched
            rbt.insert(key, idx)
        self.odd_jump = odd_jump
        self.even_jump = even_jump
        self.A = A
        #print(list(zip(range(len(A)), A, odd_jump)))
        #print(list(zip(range(len(A)), A, even_jump)))

    def good_count(self):
        even_good = set()
        odd_good = set()

        for i in range(len(self.A)):
            idx = len(self.A) - 1 - i
            if i == 0:
                even_good.add(idx)
                odd_good.add(idx)
                continue
            next_odd_idx = self.odd_jump[idx]
            if next_odd_idx in even_good:
                og = True # can make odd jump
            else:
                og = False

            next_even_idx = self.even_jump[idx]
            if next_even_idx in odd_good:
                eg = True
            else:
                eg = False
            
            if og:
                odd_good.add(idx)
                #print('add odd good', idx )
            if eg:
                even_good.add(idx)
                #print('add even good', idx)
        return len(odd_good)


### Measure Time Complexity

class elapsed_time:
    def __init__(self):
        self.start = None
        self.end = None
        self.memo = ''
        
    def __enter__(self):
        # set things up
        self.start = time.time()
        return self

    def __exit__(self, type, value, traceback):
        # tear things down
        self.end = time.time()
        #print(self.end - self.start, 'time elapsed', self.memo)

def time_complexity(length):
    A = list(range(length))
    random.shuffle(A)
    
    # print(list(zip(A, odd_jump, range(len(A)))))
    with elapsed_time() as timer:
        timer.memo = str(len(A))
        oej = OddEvenJump(A)
        #odd_jump = get_jump(A, next_odd_jump)
    elapsed = timer.end - timer.start

    return elapsed

for p in range(1, 7):
    time_list = []
    length = 10**p
    for batch in range(100):
        elapsed = time_complexity(length)
        time_list.append(elapsed)
        if elapsed == None:
            print(batch)
    print('average {}s, length={}'.format(sum(time_list)/len(time_list), length))

