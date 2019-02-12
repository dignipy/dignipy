class KMPString(str):
    def __init__(self, string):
        self._string = string
        
    def _make_match_table(self, pattern):
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
        k = 0
        table = self._make_match_table(pattern)
        for j in range(len(self)):
            if pattern[k] == self[j]:
                k += 1
                if k == len(pattern):
                    positions.append(j+1-k)
                    k = table[k]
            else:
                k == table[k]
                if k < 0:
                    k += 1
        return positions
    
    def new_find(self, pattern):
        positions = []
        k = 0
        table = self._make_match_table(pattern)
        for j in range(len(self)):
            if pattern[k] == self[j]:
                k += 1
                if k == len(pattern):
                    return j+1-k
                    k = table[k]
            else:
                k == table[k]
                if k < 0:
                    k += 1
        return None


def example():
    a = KMPString('hllajdsllaasdfelfkflallajllajdsllaasllajdsllaasdfdfdsllaasdf;dslkllajdsllaasdffjllajdsllaasdfokfaslo')
    pattern = 'llajdslla'
    print('find pattern "{}" from "{}"'.format(pattern, a))
    indices = a.kmp_search(pattern)
    print('found', indices)
    for idx in indices:
        print(a[idx:idx+len(pattern)])

if __name__ == "__main__":
    example()