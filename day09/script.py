import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

from itertools import combinations

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

PREAMBULE_LENGTH = 25 if len(sys.argv) == 1 else 5
print('Preamble length: %d\n' % PREAMBULE_LENGTH)

###########################
# region COMMON

def getFirstInvalidNumber(sequence: list) -> tuple:
    for i in range(PREAMBULE_LENGTH + 1, len(sequence)):
        preambuleSequence = sequence[i - PREAMBULE_LENGTH - 1 : i]
        validSums = set([a + b for a, b in combinations(preambuleSequence, 2)])

        if sequence[i] not in validSums:
            return (i, sequence[i])

    return None

def getContinuousSequence(sequence: list, target: int) -> list:
    for i in range(0, len(sequence) - 1):
        for j in range(i+1, len(sequence)):
            continuousSequence = sequence[i:j+1]

            total = sum(continuousSequence)
            if total > invalidNumber:
                break

            if(total == invalidNumber):
                return continuousSequence

    return None

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 1
########

sequence = [int(l) for l in lines]

(idx, invalidNumber) = getFirstInvalidNumber(sequence)
print(f'1) Number at position #{idx} does not follow cypher rule: {invalidNumber}')

########
# PART 2
########

sequence2 = [n for n in sequence if n < invalidNumber]
matchinSequence = sorted(getContinuousSequence(sequence2, invalidNumber))
print(matchinSequence)

(minNumber, maxNumber) = (matchinSequence[0], matchinSequence[-1])
print(f'2) Sum of min/max numbers from valid continuous sequence: {minNumber} + {maxNumber} = {minNumber + maxNumber}')