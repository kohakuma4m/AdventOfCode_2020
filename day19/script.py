import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re
from enum import Enum
from copy import deepcopy

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

class RULE_TYPE(Enum):
    LETTER = 0
    SUBRULES = 1

RULE_REGEX = re.compile(r'^(\d+): (\"\w\"|[\d \|]+)$')

def readRules(lines: list) -> dict:
    rules = {}
    for l in lines:
        matches = RULE_REGEX.match(l).group(1, 2)
        (ruleNumber, rule) = (matches[0], matches[1])
        if '"' in rule:
            # Must match letter
            rules[ruleNumber] = (RULE_TYPE.LETTER, rule.split('"')[1])
        else:
            # Must match all rules in order
            rules[ruleNumber] = (RULE_TYPE.SUBRULES, rule)

    return rules

def expandRules(rules: dict) -> dict:
    cRules = deepcopy(rules) # To not destroy original rules
    nbRules = len(rules.keys())

    expandedRules = { n:r[1] for n, r in cRules.items() if r[0] == RULE_TYPE.LETTER}

    isLocked = False
    while len(expandedRules.keys()) < nbRules and isLocked is False:
        isLocked = True
        for ruleNumber, ruleValue in list(expandedRules.items()):
            for n2, r2 in cRules.items():
                if n2 in expandedRules:
                    continue

                (r2Type, r2Values) = r2

                # 1) Replacing matching rule numbers in rule
                regex = f'(^({ruleNumber}) | {ruleNumber} | {ruleNumber}$|^{ruleNumber}$)' # Number at start, middle of end of rule, or single rule number
                r2Values = re.sub(regex, f' {ruleValue} ', r2Values) # Extra spaces will be remove later anyway

                # 2) Check if rule is fully expanded
                if any(c.isdigit() for c in r2Values):
                    # Rule still contains other rule numbers
                    cRules[n2] = (r2Type, r2Values)
                    continue
                else:
                    # Rule is fully expanded into letters
                    r2Values = r2Values.replace(' ', '') # Removing all spaces to create regex for rules
                    if '|' in r2Values:
                        r2Values = f'({r2Values})' # Adding regex matching group for pipe (|) operator

                    expandedRules[n2] = r2Values
                    isLocked = False

    #print('Was locked ? %s' % isLocked)

    return expandedRules

def isMessageValid(message: str, expandedRules: dict, ruleNumber: int = 0) -> bool:
    rule_regex = re.compile(f'^{expandedRules[str(ruleNumber)]}$') # Rule matching whole message
    return rule_regex.match(message) is not None

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################

(rules, messages) = utils.readFileLineGroups(filename)
rules = readRules(rules)
print(f'Number of rules: {len(rules.keys())}\nNumber of messages: {len(messages)}\n')

########
# PART 1
########

expandedRules = expandRules(rules)
validMessages = [m for m in messages if isMessageValid(m, expandedRules, ruleNumber=0)]

print('1) Number of valid messages completely matching rule "0" = %d\n' % len(validMessages))

########
# PART 2
########

# Altering rules reminder: spaces will be removed, but they must be there for expansion

# '42 | 42 8' --> 42 | 42 42 | 42 42 42 | ...
rules['8'] = (RULE_TYPE.SUBRULES, '( 42 )+') # Regex exact equivalent
print('Altering rule #08 --> %s' % rules['8'][1].replace(' ', ''))

expandedRules = expandRules(rules)
validMessages = [m for m in messages if isMessageValid(m, expandedRules, ruleNumber=0)]
nbValidMessages = len(validMessages)

depth = 2 # Depth 1 is equal to initial non altered rule #11, so we start at depth=2
while True:
    # '42 31 | 42 11 31' --> 42 31 | 42 42 31 31 | 42 42 42 31 31 31 | ...
    # No exact equivalent possible in regex, but we can increase until we get the answer for our input...
    rules['11'] = (RULE_TYPE.SUBRULES, rules['11'][1] + ' | ' + (depth * ' 42 ') + (depth * ' 31 '))
    print('Altering rule #11 --> (%s)' % rules['11'][1].replace(' ', ''))

    expandedRules = expandRules(rules)

    validMessages = [m for m in messages if isMessageValid(m, expandedRules, ruleNumber=0)]
    if len(validMessages) == nbValidMessages:
        break # We got enough for our messages
    else:
        nbValidMessages = len(validMessages)
        depth += 1

print('\n2) Number of valid messages completely matching rule "0" with altered rules = %d' % len(validMessages))