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

# Hexagonal coordinates
HexCoordinate = namedtuple('HexCoordinate2d', ['q', 'r']) # Col, row

# Get all adjacent directions in any dimensions (excluding origin)
def getAdjacentDirections(dimensions: int = 2) -> list:
    return sorted([tuple(c) for c in product([-1, 0, 1], repeat=dimensions) if c != (0,) * dimensions])

# Get all adjacent positions in any dimensions
def getAdjacentPositions(p: tuple) -> list:
    dimensions = len(p)
    return [tuple([p[i] + d[i] for i in range(dimensions)]) for d in getAdjacentDirections(dimensions)]

# Get all adjacent hexagonal positions (even row layout)
def getAdjacentHexPositions(p: tuple) -> list:
    return [
        HexCoordinate(p.q + 1, p.r), # East
        HexCoordinate(p.q + 1 if p.r % 2 == 0 else p.q, p.r - 1), # North east
        HexCoordinate(p.q + 1 if p.r % 2 == 0 else p.q, p.r + 1), # South east
        HexCoordinate(p.q - 1, p.r), # West
        HexCoordinate(p.q if p.r % 2 == 0 else p.q - 1, p.r - 1), # North west
        HexCoordinate(p.q if p.r % 2 == 0 else p.q - 1, p.r + 1) # South west
    ]

# Get Manhattan distance in between two coordinates of any dimensions
def getManhattanDistance(p1: tuple, p2: tuple):
    if len(p1) != len(p1):
        raise Exception('Coordinate dimensions does not match !')

    return sum([abs(p2[i] - p1[i]) for i in range(len(p1))])

# 2d Grid
class Grid():
    def __init__(self, data: list, printSeparator: str = '-') -> None:
        self.data = [[column for column in row] for row in data] # To be sure strings are split
        self.height = len(data)
        self.width = len(data[0]) if self.height > 0 else 0
        self.printSeparator = printSeparator

    def flipX(self):
        for y in range(self.height):
            self.data[y].reverse() # Flip all rows (horizontal flip)

    def flipY(self):
        self.data.reverse() # Flip all columns (vertical flip)

    def rotate(self, clockwise: bool = True):
        if clockwise is True:
            # Flip all columns then rotate
            self.data = [list(row) for row in list(zip(*self.data[::-1]))]
        else:
            # Flip all columns then rotate, then reverse both rows and columns again
            self.data = [list(row)[::-1] for row in list(zip(*self.data[::-1]))][::-1]

    def __str__(self) -> str:
        separator = ''.join([self.printSeparator for i in range(self.width + 2)])
        dataString = '\n'.join([' %s ' % ''.join(row) for row in self.data])
        return f'{separator}\n{dataString}\n{separator}\n'

    def colorPrint(self, colorCodes: dict = {}) -> None:
        colorString = '%s' % self
        for s, code in colorCodes.items():
            colorString = colorString.replace(s, f'{code}{s}{COLOR_CODES.LIGHT_GRAY.value}')

        print(colorString)