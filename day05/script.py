import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

FRONT = 'F'
BACK = 'B'
LEFT = 'L'
RIGHT = 'R'

NB_ROW_CHAR = 7
NB_COL_CHAR = 3
NB_COLUMNS = 8

GET_SEAT_ID = lambda row, col: NB_COLUMNS * row + col

def getPosition(code, lowerHalfChar: str, upperHalfChar: str):
    (start, end) = (0, 2 ** len(code) - 1)

    for c in code:
        range = end - start + 1
        if c == lowerHalfChar:
            end -= int(0.5 * range)
        elif c == upperHalfChar:
            start += int(0.5 * range)
        else:
            errorMsg = f'Invalid character: {c} !'
            raise NameError(errorMsg)

    if start != end:
        errorMsg = f'Invalid code: {code} !'
        raise Exception(errorMsg)

    return start

def getRow(code):
    return getPosition(code[0:7], FRONT, BACK)

def getColumn(code):
    return getPosition(code[7:10], LEFT, RIGHT)

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 1
########

seatPositions = [(getRow(code), getColumn(code)) for code in lines]
seatPositions.sort()

print('\n'.join([f'Seat ({row}, {col}): {GET_SEAT_ID(row, col)}' for (row, col) in seatPositions]), '\n')
highestSeatId = GET_SEAT_ID(seatPositions[-1][0], seatPositions[-1][1])
print('1) Highest seat ID: %d' % highestSeatId)

########
# PART 2
########

seatIds = [GET_SEAT_ID(row, col) for (row, col) in seatPositions]
missingSeatId = [seatIds[i]+1 for i in range(len(seatIds) - 1) if seatIds[i+1] == seatIds[i] + 2]
print('2) Missing seat ID: %s' % missingSeatId)