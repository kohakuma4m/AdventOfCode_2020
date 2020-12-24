import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import time

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

'''
    New optimized function version using a fixed list instead of dict (running in about 15-20s now, including time spent measuring time)

    By using a fully allocated non growing list, we remove need for try/catch on dict keys
'''
def playMemoryGame(startingNumbers: list, targetTurn: int, measureTime: bool = False) -> int:
    # History data structure to keep track of last spoken turn number for each number
    spokenNumbers = [0] * targetTurn # We won't ever speak a number equal or greater than targetTurn
    for i, n in enumerate(startingNumbers):
        spokenNumbers[n] = i + 1 # Starting number spoken turns

    # Initialization
    lastPlayedTurn = len(startingNumbers)
    lastSpokenTurn = 0

    start = time.time()
    completedPercentage = targetTurn / 10 # 10% intervals
    while lastPlayedTurn < targetTurn:
        # Note: Checking for time condition each turn adds about 5s to total time
        if measureTime and lastPlayedTurn % completedPercentage == 0:
            print('Completed %5.1f%% of turns after %.2fs' % (100 * lastPlayedTurn // targetTurn, time.time() - start))

        # Finding next spoken number
        if lastSpokenTurn == 0:
            lastSpokenNumber = 0
        else:
            lastSpokenNumber = lastPlayedTurn - lastSpokenTurn # Previous turn - last spoken turn

        # # Keeping copy of last spoken turn value for next turn
        lastSpokenTurn = spokenNumbers[lastSpokenNumber] # Keeping copy of value for next turn

        # Updating spoken number turns history
        lastPlayedTurn += 1
        spokenNumbers[lastSpokenNumber] = lastPlayedTurn # Current turn

    if measureTime:
        print('Completed %5.1f%% of turns after %.2fs' % (100.0, time.time() - start))

    return lastSpokenNumber

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

startingNumbers = [[int(n) for n in l.split(',')] for l in lines]

########
# PART 1
########

lastSpokenNumber = playMemoryGame(startingNumbers[0], targetTurn=2020)

print(f'1) The 2020th spoken number will be {lastSpokenNumber}\n')

########
# PART 2
########

TARGET_TURN = 30000000

print('Playing new %d turns game...' % TARGET_TURN)
print('----------------------------------------')
lastSpokenNumber = playMemoryGame(startingNumbers[0], targetTurn=TARGET_TURN, measureTime=True)
print('----------------------------------------')
print(f'2) The 30000000th spoken number will be {lastSpokenNumber}')