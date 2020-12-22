import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

from enum import Enum
from collections import deque, namedtuple

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

class Player(Enum):
    P1 = 1
    P2 = 2

Cards = namedtuple('Cards', ['player1', 'player2'])
GameState = namedtuple('GameState', ['player1', 'player2'])

def playCombatGame(player1Cards: list, player2Cards: list, recursive: bool = False) -> (Player, int, int):
    # Initializing new deque of cards
    cards = Cards(deque(player1Cards), deque(player2Cards))

    # Game states history
    roundsHistory = GameState(set(), set())

    # Playing game
    currentRound = 0
    while True:
        currentRound += 1

        # Initial game state
        roundInitialState = GameState(tuple(cards.player1), tuple(cards.player2)) # Copy

        if recursive is True:
            # Check rounds history to see if player 1 wins by default
            if roundInitialState.player1 in roundsHistory.player1 or roundInitialState.player2 in roundsHistory.player2:
                winner = Player.P1
                break

        # Deal next cards
        nextCard = Cards(cards.player1.popleft(), cards.player2.popleft())

        # Determine round winner
        if recursive is True and len(cards.player1) >= nextCard.player1 and len(cards.player2) >= nextCard.player2:
            # Playing sub game to determine winner
            subGameCards = Cards(list(cards.player1)[:nextCard.player1], list(cards.player2)[:nextCard.player2]) # Copy
            (roundWinner, _, _) = playCombatGame(subGameCards.player1, subGameCards.player2, recursive=True)
        else:
            # Round winner is the one with highest card value
            roundWinner = Player.P1 if nextCard.player1 > nextCard.player2 else Player.P2

        # Dealed cards go to round winner player
        if roundWinner == Player.P1:
            cards.player1.extend([nextCard.player1, nextCard.player2])
        else:
            cards.player2.extend([nextCard.player2, nextCard.player1])

        # Is the game over ?
        if len(cards.player1) == 0:
            winner = Player.P2 # Player 2 has all the cards
            break

        if len(cards.player2) == 0:
            winner = Player.P1 # Player 1 has all the cards
            break

        # Updating rounds history
        roundsHistory.player1.add(roundInitialState.player1)
        roundsHistory.player2.add(roundInitialState.player2)

    # Calculating score
    if winner == Player.P1:
        nbCards = len(cards.player1)
        score = sum([cards.player1[i] * (nbCards - i) for i in range(nbCards)])
    else:
        nbCards = len(cards.player2)
        score = sum([cards.player2[i] * (nbCards - i) for i in range(nbCards)])

    return (winner, score, currentRound)

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lineGroups = utils.readFileLineGroups(filename)

player1Cards = [int(n) for n in lineGroups[0][1:]]
player2Cards = [int(n) for n in lineGroups[1][1:]]

########
# PART 1
########

print('Playing regular combat game...')
(winner, score, nbTurns) = playCombatGame(player1Cards, player2Cards)
print(f'1) Player #{winner.value} wins after {nbTurns} rounds with score = {score}\n')

########
# PART 2
########

print('Playing recursive combat game...')
(winner, score, nbTurns) = playCombatGame(player1Cards, player2Cards, recursive=True)
print(f'2) Player #{winner.value} wins after {nbTurns} rounds with score = {score}')