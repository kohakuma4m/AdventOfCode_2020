import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

from itertools import groupby, combinations

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

CHARGING_OUTLET = 0
JOLT_THRESHOLD = 3

def getJoltJumpsForFullAdaptersChain(adaptersChain: list) -> dict:
    joltJumps = { x: 0 for x in range(1, JOLT_THRESHOLD + 1) }
    for i in range(0, len(adaptersChain) - 1):
        jumpValue = adaptersChain[i+1] - adaptersChain[i]
        joltJumps[jumpValue] += 1

    return joltJumps

# Brute force approach with loop recursion (too long obviously)
def countAllAdaptersChain(adaptersChain: list) -> int:
    chainCounts = 1

    nextAdapterIndexes = [0]
    while len(nextAdapterIndexes) > 0:
        currentIdx = nextAdapterIndexes.pop()
        currentAdapter = adaptersChain[currentIdx]

        validNextIdx = [currentIdx+1 + idx for idx, a in enumerate(adaptersChain[currentIdx+1:currentIdx+1 + JOLT_THRESHOLD]) if a - currentAdapter <= JOLT_THRESHOLD]
        if len(validNextIdx) == 0:
            continue

        chainCounts += len(validNextIdx) - 1
        nextAdapterIndexes = nextAdapterIndexes + validNextIdx

    return chainCounts

# Smarter way: we only need to count number of combinations for each subchains of multiple consecutives 1 jolt jumps
def getSubChainArrangementCounts(adaptersChain: list) -> int:
    # This only works since there are no 2 jolt jumps !
    deltas = [adaptersChain[i] - adaptersChain[i-1] for i in range(1, len(adaptersChain))]
    if 2 in deltas:
        raise Exception('Invalid solution for data')

    # Note: list must be sorted first
    subChainGroups = [[v for v in group] for key, group in groupby(deltas, lambda x: x) if key == 1]
    # Removing single 1 jolt jumps since they don't increase number of arrangements
    subChainGroups = [g for g in subChainGroups if len(g) > 1]

    subChainArrangementCounts = [len(list(combinations(g, 2))) + 1 for g in subChainGroups]
    return subChainArrangementCounts

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

sortedAdapters = sorted([int(l) for l in lines])
deviceAdapter = sortedAdapters[-1] + 3
sortedAdapters = [CHARGING_OUTLET] + sortedAdapters + [deviceAdapter]

########
# PART 1
########

joltJumps = getJoltJumpsForFullAdaptersChain(sortedAdapters)
print(joltJumps, '\n')
print(f'1) Number: {joltJumps[1]} x {joltJumps[3]} = {joltJumps[1] * joltJumps[3]}')

########
# PART 2
########

#adapterChainsCount = countAllAdaptersChain(sortedAdapters)
subChainArrangementCounts = getSubChainArrangementCounts(sortedAdapters)
totalArrangements = utils.multiplyListValues(subChainArrangementCounts)

print('\n%s\n'% subChainArrangementCounts)
print(f'2) Total number of unique adapter chains = {totalArrangements}')