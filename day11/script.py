import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error
from maplib import Coordinate, Grid, getAdjacentDirections, getAdjacentPositions # pylint: disable=import-error

from enum import Enum
from copy import deepcopy

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

class SYMBOL(Enum):
    FLOOR = '.'
    EMPTY_SEAT = 'L'
    OCCUPIED_SEAT = '#'

# For color print of non black symbols
SYMBOL_COLORS = {
    SYMBOL.EMPTY_SEAT.value: utils.COLOR_CODES.FAINT.value,
    SYMBOL.OCCUPIED_SEAT.value: utils.COLOR_CODES.BOLD.value
}

class Seat():
    def __init__(self, position: Coordinate, state: SYMBOL, adjacentSeats: list = []):
        self.position = position
        self.state = state
        self.adjacentSeats = adjacentSeats

    def isSeat(self):
        return self.state != SYMBOL.FLOOR

    def isEmpty(self):
        return self.state == SYMBOL.EMPTY_SEAT

    def isOccupied(self):
        return self.state == SYMBOL.OCCUPIED_SEAT

    def getNewState(self, switchSeatThreshold: int):
        if self.isEmpty() and all(s.isEmpty() for s in self.adjacentSeats):
            return SYMBOL.OCCUPIED_SEAT

        if self.isOccupied() and len([v for v in [s.isOccupied() for s in self.adjacentSeats] if v == True]) >= switchSeatThreshold:
            return SYMBOL.EMPTY_SEAT

        return self.state

    def __str__(self):
        return '(%s, %s) --> %s' % (self.position.x, self.position.y, self.state.name)

def mapSeats(grid: Grid) -> dict:
    seatsGrid = {}

    # Map seat grid
    for y in range(0, grid.height):
        for x in range(0, grid.width):
            s = SYMBOL(grid.data[y][x])
            if s != SYMBOL.FLOOR:
                p = Coordinate(x, y)
                seatsGrid[p] = Seat(p, s)

    return seatsGrid

def mapSeatsNeighbors(grid: Grid, seatsGrid: dict) -> None:
    for p, seat in seatsGrid.items():
        seat.adjacentSeats = [seatsGrid[p2] for p2 in getAdjacentPositions(p) if p2 in seatsGrid]

def switchSeats(grid: Grid, seatsGrid: dict, switchSeatThreshold: int):
    newGrid = deepcopy(grid)

    # Calculating all seats new state
    hasMovingSeats = False
    for p, seat in seatsGrid.items():
        newSeatState = seat.getNewState(switchSeatThreshold)
        if newGrid.data[p.y][p.x] != newSeatState.value:
            hasMovingSeats = True
            newGrid.data[p.y][p.x] = newSeatState.value

    # Updating seats with new states
    for p, seat in seatsGrid.items():
        seat.state = SYMBOL(newGrid.data[p.y][p.x])

    return (hasMovingSeats, newGrid)

def remapSeatsNeighbors(grid: Grid, seatsGrid: dict) -> None:
    directions = [Coordinate(*d) for d in getAdjacentDirections(dimensions=2)]

    # Map seat grid neighbors with new rules
    for p, seat in seatsGrid.items():
        visibleAdjacentSeats = []

        for d in directions:
            position = Coordinate(p.x, p.y)
            while utils.inbetween(0, position.x, grid.width-1) and utils.inbetween(0, position.y, grid.height-1):
                position = Coordinate(position.x + d.x, position.y + d.y)
                if position in seatsGrid:
                    visibleAdjacentSeats.append(seatsGrid[position])
                    break

        seat.adjacentSeats = visibleAdjacentSeats

def resetSeatsState(grid: Grid, seatsGrid: dict) -> None:
    for seat in seatsGrid.values():
        seat.state = SYMBOL(grid.data[seat.position.y][seat.position.x])

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 1
########

grid  = Grid(lines)
seatsGrid = mapSeats(grid)
mapSeatsNeighbors(grid, seatsGrid)
print(grid)
#print('\n'.join(['%s' % s for s in seatsGrid.values()]))
print('Number of seats: %d\n' % len(seatsGrid.keys()))

nbRounds = 0
hasMovingSeats = True
while hasMovingSeats:
    nbRounds += 1
    (hasMovingSeats, grid) = switchSeats(grid, seatsGrid, switchSeatThreshold=4)

print('Stabilization after %d rounds' % nbRounds)
grid.colorPrint(SYMBOL_COLORS)

nbOccupiedSeats = len([s for s in seatsGrid.values() if s.isOccupied()])
print('1) Number of occupied seats after stabilization: %d\n' % nbOccupiedSeats)

########
# PART 2
########

# Resetting grid to initial grid and remapping neighbors with new rules
grid = Grid(lines)
resetSeatsState(grid, seatsGrid)
remapSeatsNeighbors(grid, seatsGrid)

nbRounds = 0
hasMovingSeats = True
while hasMovingSeats:
    nbRounds += 1
    (hasMovingSeats, grid) = switchSeats(grid, seatsGrid, switchSeatThreshold=5)

print('Stabilization after %d rounds with new rules' % nbRounds)
grid.colorPrint(SYMBOL_COLORS)

nbOccupiedSeats = len([s for s in seatsGrid.values() if s.isOccupied()])
print('2) Number of occupied seats after stabilization: %d\n' % nbOccupiedSeats)