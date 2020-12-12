################################
# Mapping utils for 2D problems
################################
from typing import List, Dict
from collections import namedtuple
from enum import Enum

# ANSI COLOR CODE for color printing in terminal
class COLOR_CODES(Enum):
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

# Coordinate
Coordinate = namedtuple('Coordinate', ['x', 'y'])

def get8AdjacentDirections() -> List[Coordinate]:
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

def get8AdjacentPositions(p: Coordinate) -> List[Coordinate]:
    return [Coordinate(p.x + d.x, p.y + d.y) for d in get8AdjacentDirections()]

# Type alias
GridColumn = List[str]
GridRow = List[GridColumn]
Grid2 = List[GridRow]

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