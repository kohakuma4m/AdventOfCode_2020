import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error
import map2d as mapUtils # pylint: disable=import-error
from map2d import Grid # pylint: disable=import-error
from map3d import Coordinate3d, get3dAdjacentPositions, get3dManhattanDistance # pylint: disable=import-error

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

class Cube():
    def __init__(self, position: Coordinate3d, state: SYMBOL):
        self.position = position
        self.state = state
        self.adjacentCubes = set([])

    def isActive(self):
        return self.state == SYMBOL.ACTIVE

    def getNewState(self):
        nbActiveNeighborCubes = len([c for c in self.adjacentCubes if c.isActive()])

        if self.isActive():
            return SYMBOL.ACTIVE if utils.inbetween(2, nbActiveNeighborCubes, 3) else SYMBOL.INACTIVE
        else:
            return SYMBOL.ACTIVE if nbActiveNeighborCubes == 3 else SYMBOL.INACTIVE

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return '(%s, %s, %s) --> %s' % (self.position.x, self.position.y, self.position.z, self.state.name)

def mapCubes(grid: Grid) -> dict:
    cubesMap = {}

    # Map cubes
    for y in range(0, grid.height):
        for x in range(0, grid.width):
            s = SYMBOL(grid.data[y][x])
            p = Coordinate3d(x, y, 0)
            cubesMap[p] = Cube(p, s)

    return cubesMap

def mapCubesNeighbors(cubesMap: dict) -> None:
    newCubesMap = {}

    # Original cubes
    for p, cube in cubesMap.items():
        if len(cube.adjacentCubes) == 26:
            continue # All cube neighbors already mapped

        for p2 in get3dAdjacentPositions(p):
            if p2 in cubesMap:
                # Inner cubes (already in map)
                cube.adjacentCubes.add(cubesMap[p2])
            else:
                # Outer cubes (outside map range)
                newCube = Cube(p2, SYMBOL.INACTIVE)
                newCubesMap[p2] = newCube

    # New cubes
    for p2, newCube in newCubesMap.items():
        cubesMap[p2] = newCube # Adding new cubes to cubes map
        for p in get3dAdjacentPositions(p2):
            if p in cubesMap:
                newCube.adjacentCubes.add(cubesMap[p])
                cubesMap[p].adjacentCubes.add(newCube)
            if p in newCubesMap:
                newCube.adjacentCubes.add(newCubesMap[p])
                newCubesMap[p].adjacentCubes.add(newCube)

def runCycle(cubesMap: dict) -> None:
    # Calculate new states
    newStates = { p: cube.getNewState() for p, cube in cubesMap.items() }

    # Apply new states
    for p, newState in newStates.items():
        cubesMap[p].state = newState

def countActiveCubes(cubesMap: dict) -> int:
    return len([c for c in cubesMap.values() if c.isActive()])

def printCubesMap(cubesMap: dict) -> None:
    xPositions = [p.x for p in cubesMap.keys()]
    yPositions = [p.y for p in cubesMap.keys()]
    zPositions = [p.z for p in cubesMap.keys()]

    for z in range(min(zPositions), max(zPositions) + 1):
        print('z = %d' % z)
        for y in range(min(yPositions), max(yPositions) + 1):
            print(''.join([cubesMap[Coordinate3d(x, y, z)].state.value for x in range(min(xPositions), max(xPositions) + 1)]))
        print('\n')

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 1
########

grid = Grid(lines)
cubesMap = mapCubes(grid)
mapCubesNeighbors(cubesMap)

printCubesMap(cubesMap)
for i in range(NB_CYCLES):
    runCycle(cubesMap) # Getting new states
    mapCubesNeighbors(cubesMap) # Adding new cube neighbors
    print(f'After {i+1} cycles')
    #printCubesMap(cubesMap)

nbActiveCubes = countActiveCubes(cubesMap)
print(f'1) Number of active cubes after {NB_CYCLES} cycles = {nbActiveCubes}')