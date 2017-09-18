import time
MAX_DIF = 0.2

def simScorePairTest(arr):
    sim = int(arr[0][0]) + int(arr[1][0])
    return float(sim)


def simScorePair(p1, t1, p2, t2, lvl):
    simsqscore = 0
    simUser = 0



    for m in range(lvl):
        print("LEVEL" + str(lvl-m))
        if(m == 1):
            p1 = levelShift(p1)
            p2 = levelShift(p2)

        print(p1)
        print(t1)
        print(p2)
        print(t2)

        matches = []
        maxMatches = []
        eachMatch = []

        for i in range(len(p1)):
            for j in range(len(p2)):
                if p1[i] == p2[j]:
                    current = [0, 0, 0]
                    current[0] = i
                    current[1] = j
                    matches.append(current)

        matches.reverse()

        if len(matches) == 0:
            fakedata = [0,0,0]
            matches.append(fakedata)

        commonLoc = [None] * len(matches)
        for x in range(len(matches)):
            commonLoc[x] = [0] * len(matches)

        for l in range(1, len(matches)):
            for t in range(l-1, -1, -1):
                if matches[l][2] == 0:
                    if precTest(matches, l, t, t1, t2):
                        if commonLoc[l][t] != -1:
                            commonLoc[l][t] = 1
                        for i in range(len(matches)):
                            if commonLoc[t][i] == 1:
                                matches[i][2] = -1
        print(commonLoc)
        maximumMatch(commonLoc, len(commonLoc[0]) - 1, len(commonLoc[0]) - 1, maxMatches, eachMatch)

        if len(maxMatches) > 1:
            totalsize = 0
            for j in range(1, len(maxMatches)):
                totalsize += len(maxMatches[j-1])
                for i in range(totalsize):
                    maxMatches[j].remove(0)

        sgscore = 0

        sgscore = simScore(maxMatches)

        simsqscore = sgscore / float(len(p1) * len(p2))

        simUser += weightFunc(lvl-m) * simsqscore

    return simUser

def simScore(maxMatches):
    score = 0

    for i in range(len(maxMatches)):
        score += weightFunc(len(maxMatches[i]))

    return score


def maximumMatch(commonLoc, srow, scol, maxMatches, eachMatch):
    if outDeg(commonLoc, srow):
        eachMatch.append(srow+1)
        maxMatches.append(eachMatch)

        return

    for i in range(scol, -1, -1):
        if commonLoc[srow][i] == 1:
            eachMatch.append(srow+1)
            maximumMatch(commonLoc, i, i, maxMatches, eachMatch)

    print(maxMatches)

    return


def weightFunc(lvl):
    return int(pow(2, lvl-1))

# currently hard coded. need to implement a search by value

def levelShift(orgperson):

    shiftperson = [0 for x in orgperson]

    for i in range(len(orgperson)):
        if orgperson[i] in (1, 2, 3):
            shiftperson[i] = 11

        if orgperson[i] in (4, 5):
            shiftperson[i] = 12

    return shiftperson


def outDeg(commonLoc, srow):
    total = 0

    for i in range(len(commonLoc)):
        total += commonLoc[srow][i]

    if total:
        return False
    else:
        return True


def precTest(matches, l, t, t1, t2):
    total1 = 0
    total2 = 0
    travDif = 0
    print(l,t,t1,t2)
    print("matches", matches)

    if matches[l][0] <= matches[t][0] and matches[l][1] < matches[t][1]:
        for i in range(matches[l][0] * 2 + 1, matches[t][0] * 2):
            total1 += t1[i]

        for i in range(matches[l][1] * 2 + 1, matches[t][1] * 2):
            total2 += t2[i]

        print("total1", total1)
        print("total2", total2)
        travDif = abs(total1 - total2) / max(total1, total2)

        if travDif <= MAX_DIF:
            return True

    return False


def main():
    starttime = time.clock()

    trajectories = []

    with open('gendPpl.txt', 'r') as infile:
        for line in infile:
            p1 = [float(x) for x in line.split()]
            t1 = [float(x) for x in next(infile).split()]
            #print(p1)
            #print(t1)

            trajectories.append(p1)
            trajectories.append(t1)

    simUser = 0
    lvl = 2

    for i in range(0, len(trajectories), 2):
        currentScores = []

        for j in range(0, len(trajectories), 2):
            if i != j:
                simUser = simScorePair(trajectories[i], trajectories[i + 1], trajectories[j], trajectories[j + 1], lvl)
                currentScores.append(simUser)

        currentScoresArray = list(currentScores)

    endtime = time.clock()


main()