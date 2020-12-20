#################################
# Mapping utils for 2D+ problems
#################################
from mylib import COLOR_CODES

from collections import namedtuple
from itertools import product

# Build named tuple for coordinates in any dimensions
def buildCoordinate(dimensions: int = 2) -> namedtuple:
    names = ['x', 'y', 'z', 'w'][0:dimensions]
    for i in range(len(names), dimensions - len(names)):
        names += [f'n{i}'] # Unamed dimensions

    return namedtuple(f'Coordinate{dimensions}d', names, defaults=(0,) * len(names))

# 2, 3, 4 dimensions coordinates
Coordinate = buildCoordinate()
Coordinate3d = buildCoordinate(dimensions=3)
Coordinate4d = buildCoordinate(dimensions=4)

# Get all adjacent directions in any dimensions (excluding origin)
def getAdjacentDirections(dimensions: int = 2) -> list:
    return sorted([tuple(c) for c in product([-1, 0, 1], repeat=dimensions) if c != (0,) * dimensions])

# Get all adjacent positions in any dimensions
def getAdjacentPositions(p: tuple) -> list:
    dimensions = len(p)
    return [tuple([p[i] + d[i] for i in range(dimensions)]) for d in getAdjacentDirections(dimensions)]

# Get Manhattan distance in between two coordinates of any dimensions
def getManhattanDistance(p1: tuple, p2: tuple):
    if len(p1) != len(p1):
        raise Exception('Coordinate dimensions does not match !')

    return sum([abs(p2[i] - p1[i]) for i in range(len(p1))])

# 2d Grid
class Grid():
    def __init__(self, data: list, printSeparator: str = '-') -> None:
        self.height = len(data)
        self.width = len(data[0]) if self.height > 0 else 0
        self.data = [[column for column in row] for row in data] # To be sure strings are split
        self.printSeparator = printSeparator

    def __str__(self) -> str:
        separator = ''.join([self.printSeparator for i in range(0, self.width + 2)])
        dataString = '\n'.join([' %s ' % ''.join(row) for row in self.data])
        return f'{separator}\n{dataString}\n{separator}\n'

    def colorPrint(self, colorCodes: dict = {}) -> None:
        colorString = '%s' % self
        for s, code in colorCodes.items():
            colorString = colorString.replace(s, f'{code}{s}{COLOR_CODES.LIGHT_GRAY.value}')

        print(colorString)