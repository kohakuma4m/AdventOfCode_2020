import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re
from collections import OrderedDict

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

TICKET_RULE_REGEX = re.compile(r'^(.+): (\d+)-(\d+) or (\d+)-(\d+)$')

def findInvalidTicketValues(ticket: tuple, rules: OrderedDict) -> list:
    invalidValues = []
    for i in range(len(ticket)):
        fieldValue = ticket[i]
        if all(fieldValue not in validFieldValues for validFieldValues in rules.values()):
            invalidValues.append(fieldValue)

    return invalidValues

def findInvalidTickets(tickets: list, rules: OrderedDict) -> list:
    invalidTickets = []
    for i, t in enumerate(tickets):
        invalidValues = findInvalidTicketValues(t, rules)
        if len(invalidValues) > 0:
            invalidTickets.append((i, invalidValues))

    return invalidTickets

def findValidFieldNamesForValue(value: int, fieldNames: list, rules: OrderedDict) -> set:
    validFieldNames = set()
    for name in fieldNames:
        if value in rules[name]:
            validFieldNames.add(name)

    return validFieldNames

def findFieldNamesOrder(tickets: list, rules: OrderedDict) -> OrderedDict:
    fieldNames = [name for name in rules.keys()]
    fieldNamesOrder = { name: None for name in fieldNames }
    nbFields = len(rules.keys())
    unknownFieldPositions = [i for i in range(nbFields)]
    unknownFieldNames = [n for n in fieldNames]

    # Until all field names are identified
    while len(unknownFieldPositions) > 0:
        # Find ticket value at current position with only one matching possibility
        for pos in unknownFieldPositions:
            matchingFieldNames = set()
            for v in [t[pos] for t in tickets]: # All ticket values at current field position
                validFieldNames = findValidFieldNamesForValue(v, unknownFieldNames, rules)
                if len(matchingFieldNames) == 0:
                    matchingFieldNames = validFieldNames
                else:
                    # We only keep field names that matches with previously found valid field names
                    matchingFieldNames = matchingFieldNames.intersection(validFieldNames)

                # Short circuit to not check other values
                if len(matchingFieldNames) == 1:
                    break

            # If unique field name match
            if len(matchingFieldNames) == 1:
                matchingFieldName = matchingFieldNames.pop()
                fieldNamesOrder[matchingFieldName] = pos
                unknownFieldPositions.remove(pos)
                unknownFieldNames.remove(matchingFieldName)
                break

    # Return field name index matches sorted by position
    return OrderedDict({ position: name for name, position in sorted(fieldNamesOrder.items(), key=lambda x: x[1]) })

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lineGroups = utils.readFileLineGroups(filename)

# Rules and field names
rules = OrderedDict([])
for l in lineGroups[0]:
    (name, min1, max1, min2, max2) = TICKET_RULE_REGEX.search(l).group(1, 2, 3, 4, 5)
    rules[name] = list(range(int(min1), int(max1) + 1)) + list(range(int(min2), int(max2) + 1))

# Ticket and nearby tickets
ticket = tuple(int(n) for n in lineGroups[1][1].split(','))
nearbyTickets = [tuple(int(n) for n in l.split(',')) for l in lineGroups[2][1:]]

########
# PART 1
########

invalidTickets = findInvalidTickets(nearbyTickets, rules)
invalidValues = [v for x in invalidTickets for v in x[1]]
print('Invalid ticket values:', invalidValues)
print('\n1) Ticket scanning error rate: %d' % sum(invalidValues))

########
# PART 2
########

invalidTicketIndex = [x[0] for x in invalidTickets]
validTickets = [t for i, t in enumerate(nearbyTickets) if i not in invalidTicketIndex]

departureFields = [name for name in rules.keys() if name.startswith('departure')]
fieldNamesOrder = findFieldNamesOrder(validTickets, rules)
ticketValues = sorted([c for c in zip(fieldNamesOrder.values(), ticket)], key=lambda x: x[0])
print('\n'.join(['%s --> %s' % (k,v) for k,v in ticketValues]))

departureFieldsTicketValues = [value for name, value in ticketValues if name in departureFields]
product = utils.multiplyListValues(departureFieldsTicketValues)
print('\n2) Product of departure fields: %s = %d' % (' x '.join(['%d' % v for v in departureFieldsTicketValues]), product))