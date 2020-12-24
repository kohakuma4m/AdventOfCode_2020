import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import time

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

'''
    Original optimized version using a class (running in about 50-55s, including time spent measuring time)

    Optimized as followed:
    1) Using dictionary for history (hashable)
    2) Having loop inside of class to reduce function calls (about 10s faster)
    3) Keeping track of only last spoken turn instead of last two spoken turns for each value (about 30s faster)
       (We can use previous last spoken turns by updating history only after finding next spoken number)
'''
class MemoryGame():
    def __init__(self, startingNumbers: list):
        self.startingNumbers = startingNumbers

        # History data structure to keep track of last spoken turn number for each number
        self.spokenNumbers = { n:i+1 for i, n in enumerate(startingNumbers) }

        # Initialization
        self.lastPlayedTurn = len(startingNumbers)
        self.lastSpokenNumber = None # No starting number have been spoken before
        self.lastSpokenTurn = None

    def play(self, targetTurn: int, measureTime: bool = False) -> None:
        start = time.time()
        completedPercentage = targetTurn / 10 # 10% intervals
        while self.lastPlayedTurn < targetTurn:
            # Note: Checking for time condition each turn adds about 5s to total time
            if measureTime and self.lastPlayedTurn % completedPercentage == 0:
                print('Completed %5.1f%% of turns after %.2fs' % (100 * self.lastPlayedTurn // targetTurn, time.time() - start))

            # Finding next spoken number
            if self.lastSpokenTurn is None:
                self.lastSpokenNumber = 0
            else:
                self.lastSpokenNumber = self.lastPlayedTurn - self.lastSpokenTurn # Previous turn - last spoken turn

            # Tracking last spoken number turn (keeping copy of value for next turn)
            try:
                self.lastSpokenTurn = self.spokenNumbers[self.lastSpokenNumber]
            except KeyError:
                self.lastSpokenTurn = None # So next spoken number will be zero on next turn

            # Updating spoken number turns history
            self.lastPlayedTurn += 1
            self.spokenNumbers[self.lastSpokenNumber] = self.lastPlayedTurn # Current turn

        if measureTime:
            print('Completed %5.1f%% of turns after %.2fs' % (100.0, time.time() - start))

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

game = MemoryGame(startingNumbers[0])
game.play(targetTurn=2020)

print(f'1) The 2020th spoken number will be {game.lastSpokenNumber}\n')

########
# PART 2
########

game = MemoryGame(startingNumbers[0])

TARGET_TURN = 30000000
print('Playing new %d turns game...' % TARGET_TURN)
print('----------------------------------------')
game.play(targetTurn=TARGET_TURN, measureTime=True)
print('----------------------------------------')
print(f'2) The 30000000th spoken number will be {game.lastSpokenNumber}')