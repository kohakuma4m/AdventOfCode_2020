import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import time

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

'''
    Version 1 using list

    Optimized as followed:
    1) No list concatenations, list.pop, list.insert or list.append operations: we only edit affected list values in place
    2) Almost no list.index operations: only remaining one is for finding destination cup, since it can be anywhere ?

    But still far too slow for part 2 though, unless you want to wait a couple of hours/days
    (Estimated time of completion grows exponentially as numbers grow bigger and bigger...)
'''
def playCrabCupGame1(intialCupsOrder: list, nbMoves: int) -> (list, int):
    # Contant values
    (nbCups, minCup, maxCup) = (len(intialCupsOrder), min(intialCupsOrder), max(intialCupsOrder))

    # List of cups
    cups = intialCupsOrder[:] # Copy

    # Initialization
    currentCup = cups[0]
    currentCupIndex = 0

    start = time.time()
    for i in range(1, nbMoves+1):
        # Note: Checking for time condition each move adds about 5s to total time
        if i % 1000 == 0:
            dt = time.time() - start
            print('%-10d turns after %10.2fs --> ETA: %2.2f hours' % (i, dt, dt * (nbMoves / i) / 3600))

        # Pick three cups after current cup
        pickedCups = []
        for j in range(currentCupIndex+1, currentCupIndex+4):
            jIndex = j % nbCups
            pickedCups.append(cups[jIndex])

        # Select destination cup
        destinationCup = currentCup - 1 if currentCup > minCup else maxCup
        while destinationCup in pickedCups:
            destinationCup = destinationCup - 1 if destinationCup > minCup else maxCup

        # Next cup index (no way to deduce it, it could be anywhere...)
        destinationCupIndex = cups.index(destinationCup)

        # Move picked cups after destination cup in same order by rewriting only affected list portion in place
        if destinationCupIndex > currentCupIndex:
            j = currentCupIndex
            while True:
                j += 1
                jIndex = j % nbCups # Position to rewrite
                nextJindex = (j+3) % nbCups # Value to move
                cups[jIndex] = cups[nextJindex]

                if nextJindex == destinationCupIndex:
                    for k in range(3):
                        j += 1
                        jIndex = j % nbCups
                        cups[jIndex] = pickedCups[k]
                    break

            # Select new current cup index
            currentCupIndex = (currentCupIndex + 1) % nbCups # Current cup index didn't change
        else:
            j = currentCupIndex + 4
            while True:
                j -= 1
                jIndex = j % nbCups # Position to rewrite
                previousJindex = (j-3) % nbCups # Value to move

                if previousJindex == destinationCupIndex:
                    for k in range(1, 4):
                        cups[jIndex] = pickedCups[-k]
                        j -= 1
                        jIndex = j % nbCups
                    break
                else:
                    cups[jIndex] = cups[previousJindex]

            # Select new current cup index
            currentCupIndex = (currentCupIndex + 4) % nbCups # Current cup was move 3 position to the right

        # Select new current cup
        currentCup = cups[currentCupIndex]

    return (cups, currentCup)

'''
    Version 2 using circular linked list (implemented using a dict)

    Completes under 20 seconds...
    ...but estimated time of completion still grows exponentially (maybe a memory issue as number grows bigger ?)
'''
def playCrabCupGame2(cupsSequence: list, nbMoves: int) -> (dict, int):
    # Contant values
    (minCup, maxCup) = (min(cupsSequence), max(cupsSequence))

    # Circular linked list implementation as a dictionary (no nodes since we only have to keep track of cup value/label)
    circularDict = dict(zip(cupsSequence, cupsSequence[1:])) # Each entry points to the next like a linked list
    circularDict[cupsSequence[-1]] = cupsSequence[0] # Last entry points back to first one (circular)

    # Initialization
    currentCup = cupsSequence[0]

    start = time.time()
    for i in range(1, nbMoves + 1):
        # Note: Checking for time condition each move only adds about 2s to total time
        if i % 1000000 == 0:
            dt = time.time() - start
            print('%-8d turns after %5.2fs --> ETA: %2.2f seconds' % (i, dt, dt * (nbMoves / i)))

        # Pick three cups after current cup
        pickedCups1 = circularDict[currentCup]
        pickedCups2 = circularDict[pickedCups1]
        pickedCups3 = circularDict[pickedCups2]
        pickedCups = [pickedCups1, pickedCups2, pickedCups3]

        # Select destination cup
        destinationCup = currentCup - 1 if currentCup > minCup else maxCup
        while destinationCup in pickedCups:
            destinationCup = destinationCup - 1 if destinationCup > minCup else maxCup

        # Moving picked cups right after destination cup
        # 1) Current cup points to cup after last picked cup
        circularDict[currentCup] = circularDict[pickedCups[-1]]
        # 2) Last picked cup points to cup after destination cup
        circularDict[pickedCups[-1]] = circularDict[destinationCup]
        # 3) Destination cup points to first picked cup
        circularDict[destinationCup] = pickedCups[0]

        # Select cup after current cup as new current cup
        currentCup = circularDict[currentCup]

    return (circularDict, currentCup)

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)
print('Starting cups: ', lines[0], '\n')

########
# PART 1
########

startingCups = [int(n) for n in lines[0]]
(finalCups, currentCup) = playCrabCupGame1(startingCups, nbMoves=100)

cupOneIndex = finalCups.index(1)
finalCupsOrder = finalCups[cupOneIndex+1:] + finalCups[:cupOneIndex]

print('1) Final cup order immediately clockwise after cup #1: %s\n' % ''.join(['%s' % n for n in finalCupsOrder]))

########
# PART 2
########

startingCups2 = startingCups + [n for n in range(max(startingCups)+1, 1000000+1)] # Adding numbers up to 1 million
(finalCupsIndex, currentCup) = playCrabCupGame2(startingCups2, nbMoves=10000000) # Ten millions

nextCup = finalCupsIndex[1]
nextNextCup = finalCupsIndex[nextCup]
nextTwoCupsProduct = nextCup * nextNextCup

print('\n2) Product of two cups immediately clockwise after cup #1: %d x %d = %s' % (nextCup, nextNextCup, nextTwoCupsProduct))