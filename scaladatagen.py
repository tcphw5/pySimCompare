import random

with open('genData.csv', 'w') as f:
    f.write("src,dst,sim\n")
    numUsers = input("num users")
    # neighborList = []
    for x in range(int(numUsers)):
        # currentList = []
        for y in range(int(numUsers)):
            if random.random() > .6:
                if x != y:
                    f.write(str(x+1) + "," + str(y+1) + ".9\n")
                    f.write(str(y+1) + "," + str(x+1) + ".9\n")
                    # currentList.append(y+1)
        # neighborList.append(currentList)

# print(neighborList)