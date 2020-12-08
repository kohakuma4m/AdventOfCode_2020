import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

BIRTH_YEAR = 'byr'
ISSUE_YEAR = 'iyr'
EXPIRATION_YEAR = 'eyr'
HEIGHT = 'hgt'
HAIR_COLOR = 'hcl'
EYE_COLOR = 'ecl'
PASSPORT_ID = 'pid'
COUNTRY_ID = 'cid'

REQUIRED_PASSPORT_FIELDS = [
    BIRTH_YEAR,
    ISSUE_YEAR,
    EXPIRATION_YEAR,
    HEIGHT,
    HAIR_COLOR,
    EYE_COLOR,
    PASSPORT_ID,
    #COUNTRY_ID
]

HAIR_COLOR_REGEX = re.compile(r'^#[0-9a-f]{6}$')
EYE_COLOR_REGEX = re.compile(r'^(amb|blu|brn|gry|grn|hzl|oth)$')

def isHeightValid(v):
    if v.endswith('cm'):
        return utils.inbetween(150, int(v.replace('cm', '')), 193)
    if v.endswith('in'):
        return utils.inbetween(59, int(v.replace('in', '')), 76)
    return False

PASSPORT_FIELDS_VALIDATORS = {
    BIRTH_YEAR: lambda v: len(v) == 4 and utils.inbetween(1920, int(v), 2002),
    ISSUE_YEAR: lambda v: len(v) == 4 and utils.inbetween(2010, int(v), 2020),
    EXPIRATION_YEAR: lambda v: len(v) == 4 and utils.inbetween(2020, int(v), 2030),
    HEIGHT: lambda v: isHeightValid(v),
    HAIR_COLOR: lambda v: HAIR_COLOR_REGEX.match(v) != None,
    EYE_COLOR: lambda v: EYE_COLOR_REGEX.match(v) != None,
    PASSPORT_ID: lambda v: len(v) == 9 and v.isdigit(),
    COUNTRY_ID: lambda v: True
}

class Passport:
    def __init__(self):
        self.fields = dict()

    def __str__(self):
        return '\n'.join([f'{k} : {v}' for (k, v) in self.fields.items()])

    def isValid(self, validationFunctionName: str):
        if hasattr(self, validationFunctionName) and callable(getattr(self, validationFunctionName))\
            and validationFunctionName != 'isValid' and validationFunctionName.startswith('isValid'):
            return getattr(self, validationFunctionName)()

        errorMsg = f'Invalid validation function name: {validationFunctionName} !'
        raise NameError(errorMsg)

    def isValid1(self):
        for f in REQUIRED_PASSPORT_FIELDS:
            if f not in self.fields or self.fields[f] == '':
                return False

        return True

    def isValid2(self):
        if not self.isValid1():
            return False

        for f in REQUIRED_PASSPORT_FIELDS:
            if not PASSPORT_FIELDS_VALIDATORS[f](self.fields[f]):
                return False

        return True

def getPassports(lines):
    passports = []

    i = 0
    p = None
    while i < len(lines):
        line = lines[i]

        if line == '':
            if p != None:
                passports.append(p)
            p = None
        else:
            if p == None:
                p = Passport()

            fields = [f.split(':') for f in line.split(' ')]
            for (key, value) in fields:
                p.fields[key] = value

        i += 1

    if p != None:
        passports.append(p)

    return passports

def printInvalidPassports(passports, validationFunctionName: str):
    for idx, p in enumerate(passports):
        isValid = p.isValid(validationFunctionName)

        if not isValid:
            print('Passport #%3d: %s' % (idx + 1, isValid))
            print('\n%s\n' % p)

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 1
########

passports = getPassports(lines)

#printInvalidPassports(passports, 'isValid1')
nbValidPassports = sum([p.isValid1() for p in passports])
print('1) Number passports with all required fields: %d / %d' % (nbValidPassports, len(passports)))

########
# PART 2
########

#printInvalidPassports(passports, 'isValid2')
nbValidPassports = sum([p.isValid2() for p in passports])
print('2) Number of valid passports: %d / %d' % (nbValidPassports, len(passports)))