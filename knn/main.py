from annoy import AnnoyIndex
import random

f = 40
t = AnnoyIndex(f, "angular")
for i in range(1000):
    v = [random.gauss(0, 1) for z in range(f)]
    t.add_item(i, v)
t.build(10) # 10 trees
t.save('test.ann')

u = AnnoyIndex(f, "angular")
u.load('test.ann')

print(u.get_nns_by_item(0, 1000))
