import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re
from itertools import product

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

MASK_REGEX = re.compile(r'^mask = (.+)$')
INSTRUCTION_REGEX = re.compile(r'^mem\[(\d+)\] = (\d+)$')

def applyMask(value: int, mask: str) -> int:
    binaryValue = '%s' % f'{value:b}' # String of binary value
    maskedValue = ''
    for i in range(0, len(mask)):
        if i >= len(binaryValue): # Masked
            maskedValue = (mask[-1-i] if mask[-1-i] != 'X' else '0') + maskedValue
        elif mask[-1-i] != 'X': # Masked
            maskedValue = mask[-1-i] + maskedValue
        else: # Unchanged
            maskedValue = binaryValue[-1-i] + maskedValue

    return int(maskedValue, 2) # int to binary conversion

def applyMask2(value: int, mask: str) -> str:
    binaryValue = '%s' % f'{value:b}' # String of binary value
    maskedValue = ''
    for i in range(0, len(mask)):
        if i >= len(binaryValue): # Masked
            maskedValue = mask[-1-i] + maskedValue
        elif mask[-1-i] != '0': # Masked
            maskedValue = mask[-1-i] + maskedValue
        else: # Unchanged
            maskedValue = binaryValue[-1-i] + maskedValue

    return maskedValue

def getAllFloatingAddresses(maskedAddress: str) -> list:
    floatingBitPositions = [idx for idx, c in enumerate(maskedAddress) if c == 'X']
    nbFloatingBits = len(floatingBitPositions)

    # 2^n combinations (n = nbFloatingBits)
    floatingBitValues = product([0, 1], repeat=nbFloatingBits)

    addresses = []
    for values in floatingBitValues:
        floatingAddress = ''
        positionsValueIndex = { floatingBitPositions[i]: str(values[i]) for i in range(0, nbFloatingBits) }
        for idx in range(0, len(maskedAddress)):
            floatingAddress += positionsValueIndex[idx] if idx in floatingBitPositions else maskedAddress[idx]

        addresses.append(int(floatingAddress, 2)) # int to binary conversion

    return addresses

# Much faster version (constructing resulted address with product directly)
def getAllFloatingAddresses2(maskedAddress: str) -> list:
    options = [c if c != 'X' else ('0', '1') for c in maskedAddress]
    return [int(''.join(o),2) for o in product(*options)] # 2^n combinations (n = nbFloatingBits)

class Program:
    def __init__(self, instructions: list, memory: dict = {}):
        self.mask = None
        self.instructions = instructions
        self.nbInstructions = len(instructions)
        self.memory = memory

    def init(self):
        for line in self.instructions:
            if line.startswith('mask'):
                self.mask = MASK_REGEX.findall(line)[0]
            else:
                (idx, val) = INSTRUCTION_REGEX.findall(line)[0]
                self.memory[int(idx)] = applyMask(int(val), self.mask) # Apply mask to value

    def init2(self):
        for line in self.instructions:
            if line.startswith('mask'):
                self.mask = MASK_REGEX.findall(line)[0]
            else:
                (idx, val) = INSTRUCTION_REGEX.findall(line)[0]

                # Apply mask to index
                address = applyMask2(int(idx), self.mask)

                # Write to all floating memory address
                for floatingAddress in getAllFloatingAddresses2(address):
                    self.memory[floatingAddress] = int(val)

    def resetMemory(self):
        self.mask = None
        self.memory = {}

    def getState(self):
        return sum(self.memory.values())

    def __str__(self):
        separator = '#################'
        memory = '\n'.join(['%2d --> val: %d' % (pos, val) for pos, val in sorted(self.memory.items())])
        string = f'Number of instructions: {self.nbInstructions}\n\nCurrent memory:\n{memory}'
        return f'{separator}\n{string}\n{separator}\n'

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

########
# PART 1
########

program = Program(lines)
program.init()

print(f'1) Sum of all memory values after initialization: {program.getState()}')

########
# PART 2
########

program.resetMemory()
program.init2()

print(f'2) Sum of all memory values after initialization (version 2): {program.getState()}')