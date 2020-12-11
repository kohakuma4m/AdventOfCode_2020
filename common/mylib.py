#####################
# File utils
#####################
def readFileLines(filename):
    file = open(filename, 'r')
    lines = [line.replace('\n', '') for line in file]
    file.close()
    return lines

def readFileLineGroups(filename, groupSeparator: str = '\n\n'):
    file = open(filename, 'r')
    text = ''.join([l for l in file])
    lineGroups = [[l.replace('\n', '') for l in g.split('\n')] for g in text.split(groupSeparator)]
    file.close()
    return lineGroups

#####################
# Math utils
#####################
from functools import reduce

def inbetween(a, val, b):
    return val >= a and val <= b

def multiplyListValues(l: list):
    return reduce(lambda x, y: x * y, l , 1)