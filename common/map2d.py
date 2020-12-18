#################################
# Mapping utils for 2D+ problems
#################################
from mylib import COLOR_CODES

from typing import List, Dict
from collections import namedtuple

# Coordinate
Coordinate = namedtuple('Coordinate', ['x', 'y'])

# 3 ** 2 = 8 adjacent neighbors
def get2dAdjacentDirections() -> List[Coordinate]:
    return [
        Coordinate(0, 1), # Top
        Coordinate(0, -1), # Bottom
        Coordinate(-1, 0), # Left
        Coordinate(1, 0), # Right
        Coordinate(-1, -1), # Top left
        Coordinate(-1, 1), # Bottom left
        Coordinate(1, -1), # Top right
        Coordinate(1, 1) # Bottom right
    ]

def get2dAdjacentPositions(p: Coordinate) -> List[Coordinate]:
    return [Coordinate(p.x + d.x, p.y + d.y) for d in get2dAdjacentDirections()]

# Distance
def get2dManhattanDistance(p1: Coordinate, p2: Coordinate) -> int:
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)

# Type alias
GridColumn = List[str]
GridRow = List[GridColumn]
Grid2 = List[GridRow]

# 2d Grid
class Grid():
    def __init__(self, data: Grid2, printSeparator: str = '-') -> None:
        self.height = len(data)
        self.width = len(data[0]) if self.height > 0 else 0
        self.data = [[column for column in row] for row in data] # To be sure strings are split
        self.printSeparator = printSeparator

    def __str__(self) -> str:
        separator = ''.join([self.printSeparator for i in range(0, self.width + 2)])
        dataString = '\n'.join([' %s ' % ''.join(row) for row in self.data])
        return f'{separator}\n{dataString}\n{separator}\n'

    def colorPrint(self, colorCodes: Dict[str, str] = {}) -> None:
        colorString = '%s' % self
        for s, code in colorCodes.items():
            colorString = colorString.replace(s, f'{code}{s}{COLOR_CODES.LIGHT_GRAY.value}')

        print(colorString)