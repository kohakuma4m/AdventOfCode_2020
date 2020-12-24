import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import time

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

'''
    Same optimized version using a function instead (running in about 20-25s, including time spent measuring time)

    By using a function, we bypass all class garbage collection stuff ?
'''
def playMemoryGame(startingNumbers: list, targetTurn: int, measureTime: bool = False) -> int:
    # History data structure to keep track of last spoken turn number for each number
    spokenNumbers = { n: i+1 for i, n in enumerate(startingNumbers) }

    # Initialization
    lastPlayedTurn = len(startingNumbers)
    lastSpokenTurn = None

    start = time.time()
    completedPercentage = targetTurn / 10 # 10% intervals
    while lastPlayedTurn < targetTurn:
        # Note: Checking for time condition each turn adds about 5s to total time
        if measureTime and lastPlayedTurn % completedPercentage == 0:
            print('Completed %5.1f%% of turns after %.2fs' % (100 * lastPlayedTurn // targetTurn, time.time() - start))

        # Finding next spoken number
        if lastSpokenTurn is None:
            lastSpokenNumber = 0
        else:
            lastSpokenNumber = lastPlayedTurn - lastSpokenTurn # Previous turn - last spoken turn

        # Tracking last spoken number turn (keeping copy of value for next turn)
        try:
            lastSpokenTurn = spokenNumbers[lastSpokenNumber]
        except KeyError:
            lastSpokenTurn = None # So next spoken number will be zero on next turn

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