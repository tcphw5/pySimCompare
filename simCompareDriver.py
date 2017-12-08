from simCompare import simScorePair
from timeit import default_timer as timer

start = timer()
for x in range(10000):
    p1 = [5,3,3,2,3,1,5]
    t1 = [0,2,1,2.5,4,4,6,0]
    p2 = [3,4,2,1,4]
    t2 = [0,6,3,1,5,6,3.5,0]

    simScorePair(p1, t1, p2, t2, 2)

end = timer()

print(end - start)