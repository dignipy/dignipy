"""
Given a string s that consists of lowercase alphabets and a positive integer k return the lexicographically smallest substring of s that has length k.

Time complexity: O(n)
Space complexity: O(k)

"""

class SmallestSubstring():
    def __init__(self, s):
        self.string = s
        
    
    def calculate_prefix_len(self, max_prefix_len, new_idx, pattern_len, k, len_string):
        # To Do: 이해하기 어려움;;
        if pattern_len is None:
            return max_prefix_len
        prefix_len = max_prefix_len
        maxi = max(pattern_len, new_idx + pattern_len + k - len_string)
        if maxi < max_prefix_len:
            diff = max_prefix_len - maxi
            cnt = -(-diff//pattern_len) # same as math.ceil
            prefix_len = max_prefix_len - cnt * pattern_len
        return prefix_len


    def smallest_substring(self, k):
        string = self.string
        # state variables
        current_idx = 0
        (prefix_len, max_prefix_len, pattern_len) = (0, 0, None) # initial setting
        states_stack = [(0,0,None)] # states_stack contains states of a current minimum string's prefix

        for new_idx in range(1, len(string)):
            new_num = ord(string[new_idx])

            # check if new smallest substring will start at new_idx
            current_start_num = ord(string[current_idx])
            if current_start_num > new_num and new_idx + k - 1 < len(string):
                current_idx = new_idx
                (prefix_len, max_prefix_len, pattern_len) = (0, 0, None)
                states_stack = [(0,0,None)]
                continue
                # this is the new starting point

            # state update when current_idx changes !
            while ord(string[current_idx + prefix_len]) > new_num:
                if new_idx - prefix_len + k - 1 >= len(string):
                    # no possible new starts anymore
                    return string[current_idx:current_idx+k]
                #assert prefix_len != 0, "if prefix_len is 0, it should have been handled by the 'continue' above nonzero !"
                current_idx = new_idx - prefix_len
                if prefix_len > 1:
                    (_, max_prefix_len, pattern_len) = states_stack[prefix_len-1] # get state from the same position before
                    prefix_len = self.calculate_prefix_len(max_prefix_len, new_idx-1, pattern_len, k, len(string))
                elif prefix_len == 1:
                    (prefix_len, max_prefix_len, pattern_len) = (0, 0, None)

                while states_stack and len(states_stack) > new_idx - current_idx:
                    states_stack.pop()
                    # the 2 while loops are here only to pop() the stack. total time complexity = O(n)

            if new_idx - prefix_len + k - 1 >= len(string):
                # no possible new starts anymore
                return string[current_idx:current_idx+k]

            #assert ord(string[current_idx + prefix_len]) <= new_num, 'the other case should have been handled above'
            if ord(string[current_idx + prefix_len]) < new_num: #current_num = ord(string[current_idx + prefix_len])
                (prefix_len, max_prefix_len, pattern_len)  = (0, 0, None)
            else:
                prefix_len += 1
                max_prefix_len += 1
                # prefix_len == the length of the common prefix between current minimum string and new candidate string

                if pattern_len is None and current_idx + 2*prefix_len == new_idx + 1:
                    pattern_len = prefix_len # pattern found

                prefix_len = self.calculate_prefix_len(max_prefix_len, new_idx, pattern_len, k, len(string))

                if prefix_len == k:
                    # reset state from the same substring as previous minimum substring
                    (_, max_prefix_len, pattern_len) = states_stack[k-1]
                    prefix_len = self.calculate_prefix_len(max_prefix_len, new_idx, pattern_len, k, len(string))

            if len(states_stack) < k: # the only append is here. Thus, space complexity = O(k)
                states_stack.append((prefix_len, max_prefix_len, pattern_len))

        ans = string[current_idx:current_idx+k]
        return ans


def example():
    def left_small(string1, string2):
        for c1, c2 in zip(string1, string2):
            if ord(c1) < ord(c2):
                return True
            elif ord(c1) > ord(c2):
                return False
            else:
                continue
        # same
        return False

    def brute(string, k):
        min_string = string[:k]
        for idx in range(0, len(string)-k+1):
            if left_small(string[idx: idx+k], min_string):
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