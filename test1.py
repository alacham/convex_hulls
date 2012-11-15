import bintrees.rbtree as rbtree


tree1 = rbtree.RBTree(zip(range(1, 100,7), range(101, 200,7)))



tw = tree1.get_walker()
tw.goto(50)

for i in tw.iteritemsforward():
    print i


for i in tw.iteritemsbackward():
    print i


tree1[6:16]


[ i for i in tree1.itemslice(16, 6, reverse=True) ]







from IncrHull import *
