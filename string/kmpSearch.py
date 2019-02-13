class KMPString(str):
    @classmethod
    def _make_match_table(cls, pattern):
        table = [-1]
        cnd = 0

        for pos in range(1, len(pattern)):
            if pattern[pos] == pattern[cnd]:
                table.append(table[cnd])
            else:
                table.append(cnd)
                cnd = table[cnd]
                while cnd >= 0 and pattern[pos] != pattern[cnd]:
                    cnd = table[cnd]
            cnd += 1
        table.append(cnd)
        return table

    def kmp_search(self, pattern):
        positions = []
        j = 0
        k = 0
        table = self._make_match_table(pattern)
        while j < len(pattern):
            if self[k] == pattern[j]:
                j += 1
                k += 1
                if k == len(self):
                    positions.append(j-k)
                    k = table[k]
            else:
                k = table[k]
                if k < 0:
                    j += 1
                    k += 1
        return positions

    def kmp_find(self, pattern):
        j = 0
        k = 0
        table = self._make_match_table(pattern)
        while j < len(pattern):
            if self[k] == pattern[j]:
                j += 1
                k += 1
                if k == len(self):
                    return j-k
            else:
                k = table[k]
                if k < 0:
                    j += 1
                    k += 1
        return -1


def example():
    import time

    print(KMPString._make_match_table())
    # This example is made for kmp search to out perform built-in string.find
    #pattern = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'*10000
    pattern = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'*10000
    string = ''
    for i in range(500):
        string += pattern[:i*300]
    string += pattern
    a = KMPString(string)

    start = time.time()
    index = a.kmp_find(pattern)
    print('kmp_find', index, 'took', time.time()-start)

    start = time.time()
    index = a.find(pattern)
    print('find', index, 'took', time.time()-start)
    
    raise NotImplementedError('different results????')

if __name__ == "__main__":
    example()