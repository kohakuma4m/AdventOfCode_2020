import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

from functools import reduce

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

TREE = '#'

def countTrees(rows, slope):
    (width, height) = (len(rows[0]), len(rows))
    (x, y) = (0, 0)
    (dx, dy) = slope

    trees = []
    while y < height:
        if(rows[y % height][x % width] == TREE):
            trees.append((x, y))

        x += dx
        y += dy

    return len(trees)

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 1
########

slope = (3, 1)
nbTrees = countTrees(lines, slope)
print('1) Number of trees for slope %s = %d' %(slope, nbTrees))

########
# PART 2
########

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
counts = [countTrees(lines, s) for s in slopes]
print('2) Tree counts:')
print('\n'.join([f'{slopes[i]}: {counts[i]}' for i in range(len(slopes))]))
product = reduce(lambda a, b: a * b, counts)
print('Product: %s = %d' % (' x '.join(f'{c}' for c in counts), product))