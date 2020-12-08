import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import itertools

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# FETCH DATA
###########################

lines = utils.readFileLines(filename)

########
# PART 1
########

numbers = [int(l) for l in lines]

# Get pairs
pairs = list(itertools.combinations(numbers, 2))

# Get match
match = next(((a, b) for (a, b) in pairs if a + b == 2020), (0, 0))
(a, b) = match
print('1) Match: ', match, ' --> Product: %d x %d = %d' % (a, b, a * b))

########
# PART 2
########

# Get triplets
triplets = list(itertools.combinations(numbers, 3))

# Get match
match = next(((a, b, c) for (a, b, c) in triplets if a + b + c == 2020), (0, 0, 0))
(a, b, c) = match
print('2) Match: ', match, ' --> Product: %d x %d x %d = %d' % (a, b, c, a * b * c))