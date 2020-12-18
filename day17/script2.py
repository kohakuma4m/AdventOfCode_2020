import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error
import map2d as mapUtils # pylint: disable=import-error
from map2d import Grid # pylint: disable=import-error
from map4d import Coordinate4d, get4dAdjacentPositions # pylint: disable=import-error

from enum import Enum

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

NB_CYCLES = 6

class SYMBOL(Enum):
    INACTIVE = '.'
    ACTIVE = '#'

class Hypercube():
    def __init__(self, position: Coordinate4d, state: SYMBOL):
        self.position = position
        self.state = state
        self.adjacentHypercubes = set([])

    def isActive(self):
        return self.state == SYMBOL.ACTIVE

    def getNewState(self):
        nbActiveNeighborHypercubes = len([c for c in self.adjacentHypercubes if c.isActive()])

        if self.isActive():
            return SYMBOL.ACTIVE if utils.inbetween(2, nbActiveNeighborHypercubes, 3) else SYMBOL.INACTIVE
        else:
            return SYMBOL.ACTIVE if nbActiveNeighborHypercubes == 3 else SYMBOL.INACTIVE

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return '(%s, %s, %s, %s) --> %s' % (self.position.x, self.position.y, self.position.z, self.position.w, self.state.name)

def mapHypercubes(grid: Grid) -> dict:
    hypercubesMap = {}

    # Map cubes
    for y in range(0, grid.height):
        for x in range(0, grid.width):
            s = SYMBOL(grid.data[y][x])
            p = Coordinate4d(x, y, 0, 0)
            hypercubesMap[p] = Hypercube(p, s)

    return hypercubesMap

def mapHypercubesNeighbors(hypercubesMap: dict) -> None:
    newHypercubesMap = {}

    # Original hypercubes
    for p, hypercube in hypercubesMap.items():
        if len(hypercube.adjacentHypercubes) == 80:
            continue # All cube neighbors already mapped

        for p2 in get4dAdjacentPositions(p):
            if p2 in hypercubesMap:
                # Inner hypercubes (already in map)
                hypercube.adjacentHypercubes.add(hypercubesMap[p2])
            else:
                # Outer hypercubes (outside map range)
                newHypercube = Hypercube(p2, SYMBOL.INACTIVE)
                newHypercubesMap[p2] = newHypercube

    # New hypercubes
    for p2, newHypercube in newHypercubesMap.items():
        hypercubesMap[p2] = newHypercube # Adding new hypercubes to hypercubes map
        for p in get4dAdjacentPositions(p2):
            if p in hypercubesMap:
                newHypercube.adjacentHypercubes.add(hypercubesMap[p])
                hypercubesMap[p].adjacentHypercubes.add(newHypercube)
            if p in newHypercubesMap:
                newHypercube.adjacentHypercubes.add(newHypercubesMap[p])
                newHypercubesMap[p].adjacentHypercubes.add(newHypercube)

def runCycle(hypercubesMap: dict) -> None:
    # Calculate new states
    newStates = { p: hypercube.getNewState() for p, hypercube in hypercubesMap.items() }

    # Apply new states
    for p, newState in newStates.items():
        hypercubesMap[p].state = newState

def countActiveHypercubes(hypercubesMap: dict) -> int:
    return len([hc for hc in hypercubesMap.values() if hc.isActive()])

def printHypercubesMap(hypercubesMap: dict) -> None:
    xPositions = [p.x for p in hypercubesMap.keys()]
    yPositions = [p.y for p in hypercubesMap.keys()]
    zPositions = [p.z for p in hypercubesMap.keys()]
    wPositions = [p.w for p in hypercubesMap.keys()]

    for w in range(min(wPositions), max(wPositions) + 1):
        for z in range(min(zPositions), max(zPositions) + 1):
            print('z = %d, w = %d' % (z, w))
            for y in range(min(yPositions), max(yPositions) + 1):
                print(''.join([hypercubesMap[Coordinate4d(x, y, z, w)].state.value for x in range(min(xPositions), max(xPositions) + 1)]))
            print('\n')

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 2
########

grid = Grid(lines)
hypercubesMap = mapHypercubes(grid)
mapHypercubesNeighbors(hypercubesMap)

printHypercubesMap(hypercubesMap)
for i in range(NB_CYCLES):
    runCycle(hypercubesMap) # Getting new states
    mapHypercubesNeighbors(hypercubesMap) # Adding new hypercube neighbors
    print(f'After {i+1} cycles')
    #printHypercubesMap(hypercubesMap)

nbActiveHypercubes = countActiveHypercubes(hypercubesMap)
print(f'2) Number of active hypercubes after {NB_CYCLES} cycles = {nbActiveHypercubes}')