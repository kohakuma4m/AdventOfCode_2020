import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error
from maplib import HexCoordinate, getAdjacentHexPositions # pylint: disable=import-error

from enum import Enum
from collections import namedtuple

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

Tile = namedtuple('Tile', ['hexposition', 'color'])

class COLOR(Enum):
    BLACK = 0
    WHITE = 1

class DIRECTION(Enum):
    EAST = 'e'
    NORTH_EAST = 'ne'
    SOUTH_EAST = 'se'
    WEST = 'w'
    NORTH_WEST = 'nw'
    SOUTH_WEST = 'sw'

SINGLE_LETTER_DIRECTIONS = [DIRECTION.EAST.value, DIRECTION.WEST.value]

# Get inverse color
inverseColor = {
    COLOR.BLACK: COLOR.WHITE,
    COLOR.WHITE: COLOR.BLACK
}

# Get next hex position (even r layout)
nextHexPosition = {
    DIRECTION.EAST.value: lambda p: HexCoordinate(p.q + 1, p.r),
    DIRECTION.NORTH_EAST.value: lambda p: HexCoordinate(p.q + 1 if p.r % 2 == 0 else p.q, p.r - 1),
    DIRECTION.SOUTH_EAST.value: lambda p: HexCoordinate(p.q + 1 if p.r % 2 == 0 else p.q, p.r + 1),
    DIRECTION.WEST.value: lambda p: HexCoordinate(p.q - 1, p.r),
    DIRECTION.NORTH_WEST.value: lambda p: HexCoordinate(p.q if p.r % 2 == 0 else p.q - 1, p.r - 1),
    DIRECTION.SOUTH_WEST.value: lambda p: HexCoordinate(p.q if p.r % 2 == 0 else p.q - 1, p.r + 1)
}

def mapTiles(instructions: list) -> dict:
    tilesMap = {}

    for l in instructions:
        # Finding position of next tile to flip starting from reference tile
        i = 0; p = HexCoordinate(0, 0)
        while i < len(l):
            # Reading next direction
            d = l[i]; i += 1

            if d not in SINGLE_LETTER_DIRECTIONS:
                d += l[i]; i += 1

            # Moving to next tile position
            p = nextHexPosition[d](p)

        # FLipping tile color
        if p in tilesMap:
            tilesMap[p] = Tile(p, inverseColor[tilesMap[p].color])
        else:
            tilesMap[p] = Tile(p, COLOR.BLACK)

    return tilesMap

def countAdjacentBlackTiles(p: HexCoordinate, tilesMap: dict) -> int:
    return len([p2 for p2 in getAdjacentHexPositions(p) if p2 in tilesMap and tilesMap[p2].color == COLOR.BLACK])

def getNewTileColor(t: Tile, tilesMap: dict) -> COLOR:
    n = countAdjacentBlackTiles(t.hexposition, tilesMap)
    if t.color == COLOR.BLACK:
        return COLOR.WHITE if n == 0 or n > 2 else COLOR.BLACK
    else:
        return COLOR.BLACK if n == 2 else COLOR.WHITE

def flipTiles(tilesMap: dict) -> None:
    newTilesMap = {}

    for p, t in tilesMap.items():
        # Current tile
        if getNewTileColor(t, tilesMap) == COLOR.BLACK:
            newTilesMap[p] = Tile(p, COLOR.BLACK) # Only keeping track of black tiles

        # Tile neighbors
        for p2 in getAdjacentHexPositions(p):
            if p2 in newTilesMap:
                continue # Tile was already processed

            t2 = tilesMap[p2] if p2 in tilesMap else Tile(p2, COLOR.WHITE) # All untracked tiles are white
            if getNewTileColor(t2, tilesMap) == COLOR.BLACK:
                newTilesMap[p2] = Tile(p2, COLOR.BLACK) # Only keeping track of black tiles

    return newTilesMap

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)
print('Number of tiles to flip: %d\n' % len(lines))

########
# PART 1
########

tilesMap = mapTiles(lines)
nbBlackTiles = len([t for t in tilesMap.values() if t.color == COLOR.BLACK])

print('1) Number of black tiles after flipping all tiles in order: %d' % nbBlackTiles)

########
# PART 2
########

NB_DAYS = 100

# Flipping tiles each day for NB_DAYS
print('-------------------------------------------')
for i in range(1, NB_DAYS + 1):
    tilesMap = flipTiles(tilesMap)
    if i % 10 == 0:
        nbBlackTiles = len([t for t in tilesMap.values() if t.color == COLOR.BLACK])
        print('Number of black tiles after %3d days: %d' % (i, nbBlackTiles))
print('-------------------------------------------')

print('2) Number of black tiles after %d days: %d' % (i, nbBlackTiles))