import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error
from maplib import Grid, Coordinate3d, Coordinate4d, getAdjacentPositions # pylint: disable=import-error

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
    def __init__(self, position: tuple, state: SYMBOL, adjacentPositions: list = None):
        self.position = position
        self.state = state
        self.adjacentPositions = sorted(getAdjacentPositions(position)) if adjacentPositions is None else adjacentPositions

    def isActive(self) -> bool:
        return self.state == SYMBOL.ACTIVE

    def nbActiveNeighborCubes(self, cubesMap: dict) -> int:
        return len([p for p in self.adjacentPositions if p in cubesMap]) # Cubes map only contains active cubes

    def getNewState(self, cubesMap: dict) -> SYMBOL:
        nbActiveNeighbors = self.nbActiveNeighborCubes(cubesMap)
        if self.isActive():
            return SYMBOL.ACTIVE if utils.inbetween(2, nbActiveNeighbors, 3) else SYMBOL.INACTIVE
        else:
            return SYMBOL.ACTIVE if nbActiveNeighbors == 3 else SYMBOL.INACTIVE

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return '(%s) --> %s' % (','.join([str(self.position[i]) for i in range(len(self.position))]), self.state.name)

def runCycle(cubesMap: dict) -> dict:
    checkedCubePositions = set()
    newCubesMap = {}

    for p, cube in cubesMap.items():
        checkedCubePositions.add(p)

        # Current cube
        if cube.getNewState(cubesMap) == SYMBOL.ACTIVE:
            # Only keeping cube if it still ACTIVE
            newCubesMap[p] = Cube(p, SYMBOL.ACTIVE, cube.adjacentPositions)

        # Cubes neighbors
        for p2 in cube.adjacentPositions:
            if p2 in checkedCubePositions:
                continue # Already check when checking other cube neighbors

            checkedCubePositions.add(p2)

            if p2 in cubesMap:
                # Inner cubes (already in map)
                if cubesMap[p2].getNewState(cubesMap) == SYMBOL.ACTIVE:
                    # Only keeping cube if it still ACTIVE
                    newCubesMap[p2] = Cube(p2, SYMBOL.ACTIVE, cube.adjacentPositions)
            else:
                # Outer cubes (outside map range)
                newCube = Cube(p2, SYMBOL.INACTIVE)
                newCube.state = newCube.getNewState(cubesMap)
                if newCube.state == SYMBOL.ACTIVE:
                    # Only keeping new cube if it becomes ACTIVE
                    newCubesMap[p2] = newCube

    return newCubesMap

# Note: We only need to track ACTIVE cube, since INACTIVE cube with no ACTIVE cube neighbors will always remain INACTIVE
def mapActiveCubes(grid: Grid, Coordinate: tuple) -> dict:
    cubesMap = {}

    # Map active cubes
    for y in range(0, grid.height):
        for x in range(0, grid.width):
            s = SYMBOL(grid.data[y][x])
            if s == SYMBOL.ACTIVE:
                p = Coordinate(x, y) # Other values are zero by default
                cubesMap[p] = Cube(p, s)

    return cubesMap

def printCubesMapLayer(cubesMap: dict, dimensionCoordinates: tuple) -> None:
    xPositions = sorted([p.x for p in cubesMap.keys()])
    yPositions = sorted([p.y for p in cubesMap.keys()])

    for y in range(yPositions[0] - 1, yPositions[-1] + 2):
        s = ''
        for x in range(xPositions[0] - 1, xPositions[-1] + 2):
            p = (x, y) + dimensionCoordinates[2:]
            if p in cubesMap:
                s += cubesMap[p].state.value # Should be ACTIVE
            else:
                s += SYMBOL.INACTIVE.value
        print(s)

def printCubesMapVolume(cubesMap: dict, dimensionCoordinates: tuple) -> None:
    zPositions = sorted([p.z for p in cubesMap.keys()])
    wString = ',w = %d' % dimensionCoordinates[3] if 3 < len(dimensionCoordinates) else ''

    for z in range(zPositions[0] - 1, zPositions[-1] + 2):
        print('z = %d' % z + wString)
        printCubesMapLayer(cubesMap, (0, 0, z) + dimensionCoordinates[3:])
        print('\n')

def printHyperCubesMap(cubesMap: dict) -> None:
    wPositions = sorted([p.w for p in cubesMap.keys()])

    for w in range(wPositions[0] - 1, wPositions[-1] + 2):
        printCubesMapVolume(cubesMap, Coordinate4d(0, 0, 0, w))

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)
grid = Grid(lines)

########
# PART 1
########

cubesMap = mapActiveCubes(grid, Coordinate3d)
#printCubesMapVolume(cubesMap, dimensionCoordinates=Coordinate3d())

print('Part 1\n=============')
for i in range(NB_CYCLES):
    cubesMap = runCycle(cubesMap)
    nbActiveCubes = len(cubesMap.keys()) # Cubes map only contains active cubes
    print(f'Number of active cubes after {i+1} cycles = {nbActiveCubes}')

########
# PART 2
########

cubesMap = mapActiveCubes(grid, Coordinate4d)
#printHyperCubesMap(cubesMap)

print('\nPart 2\n=============')
for i in range(NB_CYCLES):
    cubesMap = runCycle(cubesMap)
    nbActiveCubes = len(cubesMap.keys()) # Cubes map only contains active cubes
    print(f'Number of active cubes after {i+1} cycles = {nbActiveCubes}')