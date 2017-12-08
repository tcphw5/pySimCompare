import random

with open('genData.csv', 'w') as f:
    # f.write("src,dst,sim\n")
    numUsers = input("num users")
    neighborList = []
    for x in range(int(numUsers)):
        neighborList.append([])

    for x in range(int(numUsers)):
        # currentList = []
        for y in range(int(numUsers)):
            if random.random() > .9:
                if x != y and x < y:
                    neighborList[x].append(y+1)
                    neighborList[y].append(x+1)
                    # f.write(str(x+1) + "," + str(y+1) + "\n")
                    # f.write(str(y+1) + "," + str(x+1) + "\n")
                    # currentList.append(y+1)
        # neighborList.append(currentList)

    for x in neighborList:
        for y in x:
            f.write(str(y) + " ")
        f.write("\n")

print(neighborList)

with open('genData2.csv', 'w') as f:
    f.write("UID\n")
    for x in range(int(numUsers)):
        f.write(str(x+1) + "\n")
