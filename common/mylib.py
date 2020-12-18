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
from math import gcd

# min <= value <= max
def inbetween(a, val, b):
    return val >= a and val <= b

# Product of all list values
def multiplyListValues(l: list):
    return reduce(lambda x, y: x * y, l , 1)

# Greatest common divisor of 1 or more integers: gcd(a,b,c) = gcd(gcd(a,b),c)
def greatestCommonDenominator(*numbers):
    return reduce(gcd, numbers)

# Least common multiple of 1 or more integers: lcm(a,b,c) = lcm(lcm(a,b),c)
def leastCommonMultiple(*numbers):
    def lcm(a, b):
        return (a * b) // greatestCommonDenominator(a, b)

    return reduce(lcm, numbers, 1)

#####################
# Misc utils
#####################
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