import context  # add all the submodules to sys.path

from multiwayTree import disjointSet
from graph import ZDD

print('disjointSet module:', disjointSet)
print('ZDD class:', ZDD.ZDD)

# test
zdd = ZDD.ZDD()
a = zdd.from_set(frozenset([frozenset([1])]))
print(zdd.get_set(a))
