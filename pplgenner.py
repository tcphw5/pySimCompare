import random

with open('genPpl.csv', 'w') as f:
    f.write("personID,traj\n")
    numUsers = input("num users")
    lenUser = input("len")
    locRange = input("num of locs")
    for x in range(int(numUsers)):
        f.write(str(x+1))
        f.write(",\"[")
        for y in range(int(lenUser)):
            currentRand = random.randrange(int(locRange)) + 1
            f.write("\'")
            f.write(str(currentRand))
            f.write("\',")
        f.write("\'0\',")
        for y in range(int(lenUser) + 1):
            f.write("\'")
            currentRand = random.randrange(6) + 1
            if random.random() > .5:
                currentRand += .5
            f.write(str(currentRand))
            f.write("\',")
        f.write("\'0\']\"\n")