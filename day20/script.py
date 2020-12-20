import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error
from maplib import Grid, Coordinate # pylint: disable=import-error

from enum import Enum

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

class SYMBOL(Enum):
    SEA = '.'
    HAZARD = '#'
    SEA_MONSTER = 'O'

# For color print of non black symbols
SYMBOL_COLORS = {
    SYMBOL.SEA.value: utils.COLOR_CODES.FAINT.value,
    SYMBOL.HAZARD.value: utils.COLOR_CODES.LIGHT_BLUE.value,
    SYMBOL.SEA_MONSTER.value: utils.COLOR_CODES.LIGHT_GREEN.value
}

class BORDER_TYPE(Enum):
    TOP = 'T'
    BOTTOM = 'B'
    LEFT = 'L'
    RIGHT = 'R'

class ORIENTATION(Enum):
    HORIZONTAL = 'H'
    VERTICAL = 'V'

BORDER_TYPE_ORIENTATION = {
    # Clockwise direction: perpendicular direction on the left
    BORDER_TYPE.TOP: ORIENTATION.VERTICAL,
    BORDER_TYPE.LEFT: ORIENTATION.HORIZONTAL,
    BORDER_TYPE.BOTTOM: ORIENTATION.VERTICAL,
    BORDER_TYPE.RIGHT: ORIENTATION.HORIZONTAL
}

OPPOSITE_DIRECTION = {
    # Current direction: opposite direction
    BORDER_TYPE.TOP: BORDER_TYPE.BOTTOM,
    BORDER_TYPE.BOTTOM: BORDER_TYPE.TOP,
    BORDER_TYPE.LEFT: BORDER_TYPE.RIGHT,
    BORDER_TYPE.RIGHT: BORDER_TYPE.LEFT
}

NEXT_CLOCKWISE_DIRECTION = {
    # Current direction: next clockwise direction
    BORDER_TYPE.TOP: BORDER_TYPE.RIGHT,
    BORDER_TYPE.RIGHT: BORDER_TYPE.BOTTOM,
    BORDER_TYPE.BOTTOM: BORDER_TYPE.LEFT,
    BORDER_TYPE.LEFT: BORDER_TYPE.TOP,
}

ADJACENT_POSITION = {
    # Current direction: next position
    BORDER_TYPE.TOP: lambda p: Coordinate(p.x, p.y - 1),
    BORDER_TYPE.BOTTOM: lambda p: Coordinate(p.x, p.y + 1),
    BORDER_TYPE.LEFT: lambda p: Coordinate(p.x - 1, p.y),
    BORDER_TYPE.RIGHT: lambda p: Coordinate(p.x + 1, p.y)
}

class PuzzlePieceBorder():
    def __init__(self, type: BORDER_TYPE, data: list):
        self.type = type
        self.data = data

    def __str__(self):
        if self.type == BORDER_TYPE.TOP or self.type == BORDER_TYPE.BOTTOM:
            return ''.join(self.data)
        else:
            return '\n'.join(self.data)

class PuzzlePiece():
    def __init__(self, id: str, grid: Grid):
        self.id = id
        self.grid = grid
        self.data = self.grid.data
        self.rotated = 0
        self.xFlipped = False
        self.yFlipped = False
        self.matchingPiece = { b: set() for b in BORDER_TYPE }

    def getBorder(self, b: BORDER_TYPE) -> PuzzlePieceBorder:
        if b == BORDER_TYPE.TOP:
            return PuzzlePieceBorder(BORDER_TYPE.TOP, self.data[0][:])
        if b == BORDER_TYPE.BOTTOM:
            return PuzzlePieceBorder(BORDER_TYPE.BOTTOM, self.data[-1][:])
        if b == BORDER_TYPE.LEFT:
           return PuzzlePieceBorder(BORDER_TYPE.LEFT, [row[0] for row in self.data])
        if b == BORDER_TYPE.RIGHT:
           return PuzzlePieceBorder(BORDER_TYPE.RIGHT, [row[-1] for row in self.data])

    def getNbMatchingPieces(self):
        return len([p.id for b in BORDER_TYPE for p in self.matchingPiece[b]])

    def flipX(self):
        self.grid.flipX()
        self.xFlipped = not self.xFlipped

        # Flipping matching pieces directions
        temp = self.matchingPiece[BORDER_TYPE.LEFT]
        self.matchingPiece[BORDER_TYPE.LEFT] = self.matchingPiece[BORDER_TYPE.RIGHT]
        self.matchingPiece[BORDER_TYPE.RIGHT] = temp

    def flipY(self):
        self.grid.flipY()
        self.yFlipped = not self.yFlipped

        # Flipping matching pieces directions
        temp = self.matchingPiece[BORDER_TYPE.TOP]
        self.matchingPiece[BORDER_TYPE.TOP] = self.matchingPiece[BORDER_TYPE.BOTTOM]
        self.matchingPiece[BORDER_TYPE.BOTTOM] = temp

    def rotate(self, clockwise: bool = True):
        self.grid.rotate(clockwise)
        self.data = self.grid.data
        self.rotated = (self.rotated + (90 if clockwise is True else 270)) % 360

        # Rotating matching pieces directions
        if clockwise is True:
            temp = self.matchingPiece[BORDER_TYPE.TOP]
            self.matchingPiece[BORDER_TYPE.TOP] = self.matchingPiece[BORDER_TYPE.LEFT]
            self.matchingPiece[BORDER_TYPE.LEFT] = self.matchingPiece[BORDER_TYPE.BOTTOM]
            self.matchingPiece[BORDER_TYPE.BOTTOM] = self.matchingPiece[BORDER_TYPE.RIGHT]
            self.matchingPiece[BORDER_TYPE.RIGHT] = temp
        else:
            temp = self.matchingPiece[BORDER_TYPE.TOP]
            self.matchingPiece[BORDER_TYPE.TOP] = self.matchingPiece[BORDER_TYPE.RIGHT]
            self.matchingPiece[BORDER_TYPE.RIGHT] = self.matchingPiece[BORDER_TYPE.BOTTOM]
            self.matchingPiece[BORDER_TYPE.BOTTOM] = self.matchingPiece[BORDER_TYPE.LEFT]
            self.matchingPiece[BORDER_TYPE.LEFT] = temp

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return 'Id: %s; rotated: %d, flipped (x,y): (%i, %i)' % (self.id, self.rotated, self.xFlipped, self.yFlipped)

class Puzzle():
    def __init__(self, pieces: dict):
        self.pieces = pieces
        self.nbPieces = len(self.pieces.keys())

        # Finding all matching pieces
        self._findMatchingPieces()

        # Classify piece type
        self.cornerPieces = set([p for id, p in self.pieces.items() if p.getNbMatchingPieces() == 2])
        self.sidePieces = set([p for id, p in self.pieces.items() if p.getNbMatchingPieces() == 3])
        self.middlePieces = set([p for id, p in self.pieces.items() if p.getNbMatchingPieces() == 4])

        self.matchedPiecePositions = {}

    def _findMatchingPieces(self) -> None:
        print('Organizing puzzle pieces...\n')

        # Current piece stays fixed when searching for matching pieces
        for p in self.pieces.values():
            # Find all valid adjacent pieces, in any orientation or flipped state
            for p2 in self.pieces.values():
                if p2 == p:
                    continue

                for b in BORDER_TYPE:
                    pieceBorder = p.getBorder(b).data
                    reversePuzzlePieceBorder = pieceBorder[::-1]

                    for b2 in BORDER_TYPE:
                        t2Border = p2.getBorder(b2).data
                        if t2Border == pieceBorder or t2Border == reversePuzzlePieceBorder:
                            p.matchingPiece[b].add(p2)
                            p2.matchingPiece[b2].add(p)

    @staticmethod
    def _printMatchingPieces(pieces: list) -> None:
        for p in pieces:
            print(p.id, ['%s: %s' % (b.name, p2.id) for b in BORDER_TYPE for p2 in p.matchingPiece[b]])
        print()

    def printMatchingPieces(self, printPieces: bool = False) -> None:
        print('Corner pieces: %d' % len(self.cornerPieces))
        if printPieces:
            self._printMatchingPieces(self.cornerPieces)

        print('Side pieces: %d' % len(self.sidePieces))
        if printPieces:
            self._printMatchingPieces(self.sidePieces)

        print('Middle pieces: %d' % len(self.middlePieces), '\n')
        if printPieces:
            self._printMatchingPieces(self.middlePieces)

    def _findStartingCorner(self) -> PuzzlePiece:
        startingCorner = next(iter(self.cornerPieces))

        # Flipping corner so it's in right orientation in top left corner
        if len(startingCorner.matchingPiece[BORDER_TYPE.TOP]) == 1:
            startingCorner.flipY()
        if len(startingCorner.matchingPiece[BORDER_TYPE.LEFT]) == 1:
            startingCorner.flipX()

        return startingCorner

    def solve(self, log=False) -> None:
        # Warning: currrent solving solution only works if each puzzle piece borders match with a single other puzzle piece !
        if set([p for id, p in self.pieces.items() if p.getNbMatchingPieces() > 4]):
            raise Exception('Solution cannot work for puzzle with non unique matching piece borders !')

        if len(self.matchedPiecePositions.keys()) > 0:
            return # Already solved

        print('Solving puzzle...\n------------------')

        # 1) Starting with any corner in fixed orientation
        startingCorner = self._findStartingCorner()

        # 2) Adding all pieces clockwise in a spiral from starting corner
        matchedPieces = set()
        currentPiece = startingCorner
        currentPosition = Coordinate(0,0)
        currentDirection = BORDER_TYPE.RIGHT
        while True:
            # Adding current piece to solved puzzle
            matchedPieces.add(currentPiece)
            self.matchedPiecePositions[currentPosition] = currentPiece

            # Finding next piece
            nextPiece = next(iter(currentPiece.matchingPiece[currentDirection]))
            if nextPiece in matchedPieces:
                if len(matchedPieces) == self.nbPieces:
                    break # Done, all pieces are matched

                # Changing direction inward
                currentDirection = NEXT_CLOCKWISE_DIRECTION[currentDirection]
                nextPiece = next(iter(currentPiece.matchingPiece[currentDirection]))

            if log:
                print('(%s, %s) currentPiece %s --> %s --> %s' % (currentPosition.x, currentPosition.y, currentPiece.id, currentDirection.name, nextPiece.id))

            # Flipping / rotating next piece until adjacent border matched
            oppositeDirection = OPPOSITE_DIRECTION[currentDirection]
            currentBorderToMatch = currentPiece.getBorder(currentDirection).data
            currentFlippedBorderToMatch = currentBorderToMatch[::-1]
            while currentBorderToMatch != nextPiece.getBorder(oppositeDirection).data:
                if currentFlippedBorderToMatch == nextPiece.getBorder(oppositeDirection).data:
                    if BORDER_TYPE_ORIENTATION[currentDirection] == ORIENTATION.HORIZONTAL:
                        nextPiece.flipY()
                    else:
                        nextPiece.flipX()
                else:
                    nextPiece.rotate()

            # Moving to next piece
            currentPiece = nextPiece
            currentPosition = ADJACENT_POSITION[currentDirection](currentPosition)
            if nextPiece in self.cornerPieces:
                # Changing direction at border (so we don't leave puzzle area)
                currentDirection = NEXT_CLOCKWISE_DIRECTION[currentDirection]

        print('------------------\n')

    def printCompletedPuzzlePieceIDs(self) -> None:
        xMax = max([p.x for p in self.matchedPiecePositions.keys()])
        yMax = max([p.y for p in self.matchedPiecePositions.keys()])

        separator = '---'.join(['-'*4 for i in range(xMax + 1)]) + '------'

        print('Completed puzzle:')
        print(separator)
        for y in range(yMax + 1):
            print('| ', '   '.join([self.matchedPiecePositions[Coordinate(x,y)].id for x in range(xMax + 1)]), ' |')
        print(separator, '\n')

# Create tiles
def readPieces(lineGroups: list) -> dict:
    tiles = {}
    for lines in lineGroups:
        tileId = lines[0].replace('Tile ', '').replace(':', '')
        tileData = Grid(lines[1:])
        tiles[tileId] = PuzzlePiece(tileId, tileData)

    return tiles

def getCompletedPuzzleCleanedImage(imagePuzzle: Puzzle) -> Grid:
    # Removing puzzle piece borders
    cleanedPiecesData = {}
    for p in imagePuzzle.pieces.values():
        cleanedPiecesData[p.id] = [[p.grid.data[y][x] for x in range(1, p.grid.width -1)] for y in range(1, p.grid.height - 1)]

    # Each pieces have same dimensions
    piecesWidth = Grid(next(iter(cleanedPiecesData.values()))).width
    piecesHeight = Grid(next(iter(cleanedPiecesData.values()))).height

    # Puzzle dimensions
    puzzleWidth = max([p.x for p in imagePuzzle.matchedPiecePositions.keys()]) + 1
    puzzleHeight = max([p.y for p in imagePuzzle.matchedPiecePositions.keys()]) + 1

    # Joining pieces together
    fullImage = [[SYMBOL.SEA.value for x in range(piecesWidth * puzzleWidth)] for y in range(piecesHeight * puzzleHeight)]
    for py in range(puzzleHeight):
        for px in range(puzzleWidth):
            puzzlePieceId = imagePuzzle.matchedPiecePositions[Coordinate(px, py)].id
            for y in range(piecesHeight):
                for x in range(piecesWidth):
                    fullImage[py * piecesHeight + y][px * piecesWidth + x] = cleanedPiecesData[puzzlePieceId][y][x]

    return Grid(fullImage)

def findSeaMonsters(image: Grid, seaMonster: Grid) -> int:
    # Keep only positions to match
    seaMonsterMatchingPositions = set()
    for y in range(seaMonster.height):
        for x in range(seaMonster.width):
            if seaMonster.data[y][x] == SYMBOL.HAZARD.value:
                seaMonsterMatchingPositions.add(Coordinate(x, y))

    # Find all sea monsters
    seaMonstersCount = 0

    y = 0
    while y + seaMonster.height < image.height:
        x = 0
        while x + seaMonster.width < image.width:
            # Check if sea monster in current view
            seaMonsterVisible = all(image.data[y + p.y][x + p.x] == SYMBOL.HAZARD.value for p in seaMonsterMatchingPositions)

            if seaMonsterVisible is True:
                # Increasing sea monsters count
                seaMonstersCount += 1

                # Marking sea monster on image
                for p in seaMonsterMatchingPositions:
                    image.data[y + p.y][x + p.x] = SYMBOL.SEA_MONSTER.value

                # Skipping to next possible non overlapping sea monster
                x += seaMonster.width
            else:
                x += 1

        if seaMonsterVisible is True:
            # Skipping to next possible non overlapping sea monster
            y += seaMonster.height
        else:
            y += 1

    return seaMonstersCount

def countSeaMonstersAndOrientImage(image: Grid, seaMonster: Grid) -> int:
    nbSeaMonster = findSeaMonsters(image, SEA_MONSTER)

    for i in range(4):
        if nbSeaMonster > 0:
            break

        # Trying rotation first
        image.rotate()
        nbSeaMonster = findSeaMonsters(image, SEA_MONSTER)

    if nbSeaMonster == 0:
        image.flipX() # Flip horizontaly and retry

    for i in range(4):
        if nbSeaMonster > 0:
            break

        # Retrying rotation in flipped position
        image.rotate()
        nbSeaMonster = findSeaMonsters(image, SEA_MONSTER)

    return nbSeaMonster

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################

# Sea monster pattern
SEA_MONSTER = Grid([
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
])

lineGroups = utils.readFileLineGroups(filename)

pieces = readPieces(lineGroups)
print('Number of pieces: %d\n' % len(pieces.keys()))

########
# PART 1
########

# Create puzzle
imagePuzzle = Puzzle(pieces)
imagePuzzle.printMatchingPieces(printPieces=False)

product = utils.multiplyListValues([int(piece.id) for piece in imagePuzzle.cornerPieces])
print('1) Corner pieces product: %d\n' % product)

########
# PART 2
########

# Solve puzzle
imagePuzzle.solve(log=True)
imagePuzzle.printCompletedPuzzlePieceIDs()

# Extract image
image = getCompletedPuzzleCleanedImage(imagePuzzle)

print('Searching for sea monsters...\n%s' % SEA_MONSTER)
nbSeaMonster = countSeaMonstersAndOrientImage(image, SEA_MONSTER)
print('Image with sea monsters:')
image.colorPrint(SYMBOL_COLORS)
print('Number of sea monsters: %d\n' % nbSeaMonster)

nbHazards = len([1 for y in range(image.height) for x in range(image.width) if image.data[y][x] == SYMBOL.HAZARD.value])
print('2) Number of non sea monster hazard = %d' % nbHazards)