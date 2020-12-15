import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

class MemoryGame():
    def __init__(self, startingNumbers: list):
        self.startingNumbers = startingNumbers
        self.spokenNumbers = { n: [i+1] for i, n in enumerate(startingNumbers) }
        self.lastSpokenNumber = startingNumbers[-1]
        self.lastPlayedTurn = len(startingNumbers)

    def __str__(self):
        return f'Current turn: {self.lastPlayedTurn}\nLast spoken number: {self.lastSpokenNumber}'

    def playTurn(self):
        currentTurn = self.lastPlayedTurn + 1
        lastSpokenNumberTurns = self.spokenNumbers[self.lastSpokenNumber] if self.lastSpokenNumber in self.spokenNumbers else None

        # Getting next spoken number
        if lastSpokenNumberTurns is None or len(lastSpokenNumberTurns) < 2:
            currentSpokenNumber = 0 # Number was spoken less than twice before
        else:
            currentSpokenNumber = lastSpokenNumberTurns[-1] - lastSpokenNumberTurns[-2] # Last two turns number was spoken

        # Updating spoken number turns history
        if currentSpokenNumber in self.spokenNumbers:
            self.spokenNumbers[currentSpokenNumber] = [self.spokenNumbers[currentSpokenNumber][-1], currentTurn] # Keeping only two last values
        else:
            self.spokenNumbers[currentSpokenNumber] = [currentTurn]

        self.lastSpokenNumber = currentSpokenNumber
        self.lastPlayedTurn = currentTurn

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
while game.lastPlayedTurn < 2020:
    game.playTurn()

print(f'1) The 2020th spoken number will be {game.lastSpokenNumber}')

########
# PART 2
########

game = MemoryGame(startingNumbers[0])

TARGET_TURN = 30000000
completedPercentage = TARGET_TURN / 20
while game.lastPlayedTurn < 30000000:
    game.playTurn()
    if game.lastPlayedTurn % completedPercentage == 0:
        print(f'Completed {100 * completedPercentage // TARGET_TURN}% of turns')
        completedPercentage += TARGET_TURN / 20

print(f'2) The 30000000th spoken number will be {game.lastSpokenNumber}')