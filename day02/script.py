import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re

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

pattern = re.compile(r'^(\d+)-(\d+) (\w+): (\w+)$')
passwordData = [(int(min), int(max), letter, password) for (min, max, letter, password) in [pattern.findall(l)[0] for l in lines]]

validPasswords = [password for (min, max, letter, password) in passwordData if utils.inbetween(min, password.count(letter), max)]
print('1) Number of valid passwords: ', len(validPasswords), '/ %d' % len(passwordData))

########
# PART 2
########

def isValid(pos1, pos2, letter, password):
    sum = 0
    if password[pos1 - 1] == letter:
        sum += 1
    if password[pos2 - 1] == letter:
        sum += 1
    return sum == 1

validPasswords = [password for (a, b, letter, password) in passwordData if isValid(a, b, letter, password)]
print('2) Number of valid passwords: ', len(validPasswords), '/ %d' % len(passwordData))