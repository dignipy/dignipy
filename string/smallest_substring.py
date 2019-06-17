"""
Given a string s that consists of lowercase alphabets and a positive integer k,
return the lexicographically smallest substring of s that has length k.

Time complexity: O(n)
Space complexity: O(k)

"""

class SmallestSubstring():
    def __init__(self, s):
        self.string = s

    def smallest_substring(self, k):
        string = self.string
        current_idx = 0
        # new_idx = 0
        prefix_len = 0
        # current_idx: the starting index of current smallest string.
        # new_idx: the index of the character that we want to compare to a character in current smallest string.
        # prefix_len: the length of current smallest string's prefix that is the same as a substring ending at new_idx.
        # in other words, string[current_idx: current_idx + prefix_len] == string[new_idx-prefix_len: new_idx]

        stack = [prefix_len] # stack contains the current smallest substring's prefix_lens
        # stack stores prefix_len data in case another substring with a same prefix becomes a new smallest substring.
        # in such a case, we reuse stack[:prefix_len] of the stack and pop the rest
        for new_idx in range(1, len(string)):
            new_char = string[new_idx]
            current_start_char = string[current_idx]
            if current_start_char > new_char and new_idx + k - 1 < len(string):
                current_idx = new_idx
                prefix_len = 0
                stack = [prefix_len]
                continue
            while string[current_idx + prefix_len] > new_char:
                if new_idx - prefix_len + k - 1 >= len(string):
                    return string[current_idx:current_idx+k]
                # note that if prefix_len == 0, current_idx = new_idx so while loop exits after one loop:
                current_idx = new_idx - prefix_len
                if stack and len(stack) > prefix_len:
                    del stack[prefix_len:] # multiple pop()s
                    # the while loop is here only to pop() the stack. total time complexity = O(n)
                if prefix_len >= 1:
                    prefix_len = stack[prefix_len-1] # get state from the same position before
                    # note that stack[i] <= i holds, so prefix_len always decreases
                    # this while loop only decreses len(stack)
                    # number of items to be deleted is at most the number of items appended
                    # total number of items that are appended is at most n
                    # thus total time consumed by the while loop is at most O(n) throughout the entire code.

            if new_idx - prefix_len + k - 1 >= len(string):
                return string[current_idx:current_idx+k]
            if string[current_idx + prefix_len] < new_char:
                prefix_len = 0
            else: # string[current_idx + prefix_len] == new_char:
                prefix_len += 1
                if prefix_len == k:
                    prefix_len = stack[k-1]
            if len(stack) < k: # the only append is here. Thus, space complexity = O(k)
                stack.append(prefix_len)
        ans = string[current_idx:current_idx+k]
        return ans


##################################################
############### SOME EXPLANATIONS ################
##################################################
# string:      a x y w z z a x y b ...
# stack:       0 0 0 0 0 0 1 2 3
# current_idx  ^
# at this point we know that current_idx will change to 6 since 'w' > 'b'.
# before getting the new prefix length for b, we want to update the stack by deleting stack[3:]

# string:      a x y b ...
# stack:       0 0 0 0
# current_idx  ^

# In this way, we can reuse stack elements corresponding to 'axy'

##################################################
# at every step, we check if the new character is smaller than the current starting character:
# string:      b c d e a ...
# stack:       0 0 0 0
# current_idx  ^

# since 'b' > 'a', 
# string:      b c d e a ...
# stack:               0
# current_idx          ^

##################################################
# the reason we have while loop:
# current_idx can change multiple times before new prefix_len is appended

# string:      a b c a b c a b a
# stack:       0 0 0 1 2 3 4 5
# current_idx  ^

# we reuse the stack corresponding to "abcab"
# since 'c' > 'a', 
# string:      a b c a b c a b a
# stack:             0 0 0 1 2
# current_idx        ^

# we reuse the stack corresponding to "ab"
# since 'c' > 'a',
# string:      a b c a b c a b a
# stack:                   0 0 1
# current_idx              ^

##################################################
# k = 3
# string:      a b c d e f g a b c ...
# stack:       0 0 0
# prefix_len   0 0 0 0 0 0 0 1 2
# current_idx  ^

# since k == 3, prefix_len for index 9 will be 0
# we can assume that we hadn't seen "defgabc" and start over

# note that we reuse prefix_len many elements from the beginning of the statck, 
# the stack doesn't need to be longer than k
##################################################


def example():
    def brute(string, k):
        min_string = string[:k]
        for idx in range(0, len(string)-k+1):
            if string[idx: idx+k] < min_string:
                min_string = string[idx: idx+k]
        return min_string

    import random
    random.seed(87)
    n = 1000
    for test_case in range(100000):
        tmp_strs = []
        for _ in range(n):
            if random.random() > 0.5:
                tmp_strs.append('b')
            else:
                tmp_strs.append('a')
        string = ''.join(tmp_strs)
        k = random.randint(1,n-1)
        ss = SmallestSubstring(string)
        assert ss.smallest_substring(k) == brute(string, k), 'string={}, k={}'.format(string, k)

        if not test_case%10000:
            print(test_case)
    print('all okay')

    
if __name__ == "__main__":
    example()