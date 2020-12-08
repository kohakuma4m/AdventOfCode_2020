import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

RULE_REGEX = re.compile(r'^(.+) bags contain ((\d+) (.+?) bags?,?|no other bags)+\.$')

def generateBagTypesAndContentMap(lines: list, printRules: bool = False):
    contentMap = {}

    for l in lines:
        t = None
        if 'no other bags' in l:
            t = RULE_REGEX.search(l).group(1)
            contentMap[t] = []
        elif ',' not in l:
            (t, n1, t1) = RULE_REGEX.search(l).group(1, 3, 4)
            contentMap[t] = [(t1, int(n1))]
        else:
            subRegex = ', '.join(['(\d+) (.+?) bags?' for i in range(0, l.count(',') + 1)])
            SUB_RULE_REGEX = re.compile(r'^(.+) bags contain ' + subRegex + r'\.$')
            matchinGroups = SUB_RULE_REGEX.search(l).groups()
            nbGroups = len(matchinGroups)
            t = matchinGroups[0]
            contentMap[t] = [(matchinGroups[i+1], int(matchinGroups[i])) for i in range(1, nbGroups - 1, 2)]

        if printRules:
            print('%-15s --> ' % t, contentMap[t])

    if printRules:
        print('\n')

    types = contentMap.keys()
    return (types, contentMap)

def getBagsTotal(bagTypeContentMap: dict, bagType: str, bags: dict, qty: int = 1):
    content = bagTypeContentMap[bagType]

    if len(content) == 0:
        return bags

    for (t, n) in content:
        m = qty * n # Multipler for recursive counting

        if t not in bags:
            bags[t] = m
        else:
            bags[t] = bags[t] + m
        getBagsTotal(bagTypeContentMap, t, bags, m)

    return bags

def containBag(bagType: str, bags: dict):
    return bagType in bags and bags[bagType] > 0

def printContent(bags):
    for (t, c) in bags:
        print('%s:' % t, '\n========')
        print('\n'.join([f'{bag}: {count}' for (bag, count) in c.items()]), '\n')

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

(bagTypes, bagTypesContentMap) = generateBagTypesAndContentMap(lines)#, printRules=True)

########
# PART 1
########

STARTING_BAG = 'shiny gold'

bagContents = { t: getBagsTotal(bagTypesContentMap, t, {}) for t in bagTypes }
#printContent(bagContents)

nbBags = sum([1 if containBag(STARTING_BAG, c) else 0 for c in bagContents.values()])
print('1) Number of bag types that can contain %s bag type = %d' % (STARTING_BAG, nbBags))

########
# PART 2
########

startingBagContent = bagContents[STARTING_BAG]
#print(startingBagContent)

totalBags = sum([count for count in startingBagContent.values()])
print('2) Total number of bags inside %s bag type = %d' % (STARTING_BAG, totalBags))