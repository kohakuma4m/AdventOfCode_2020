import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

from enum import Enum
from collections import OrderedDict

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

class INSTRUCTIONS(Enum):
    acc = 1 # Accumulator
    jmp = 2 # Jump
    nop = 3 # No operation

    def __str__(self):
        return '%s' % self.name

EXECUTE_RULE = {
    INSTRUCTIONS.acc: lambda state, value: state.update(acc = state.acc + value, pos = state.pos + 1),
    INSTRUCTIONS.jmp: lambda state, value: state.update(pos = state.pos + value),
    INSTRUCTIONS.nop: lambda state, value: state.update(pos = state.pos + 1)
}

class Program:
    def __init__(self, instructions: list, pos: int = 0, acc: int = 0):
        self.instructions = instructions
        self.nbInstructions = len(instructions)
        self.executedInstructions = OrderedDict([])
        (self.pos, self.acc) = (pos, acc)

    def run(self):
        while not self.isLooping() and not self.isTerminated():
            self.executedInstructions[self.pos] = self.acc
            (instruction, value) = self.instructions[self.pos]
            EXECUTE_RULE[instruction](self, value)

    def isTerminated(self):
        return self.pos >= self.nbInstructions

    def isLooping(self):
        return self.pos in self.executedInstructions.keys()

    def update(self, acc = None, pos = None):
        self.acc = self.acc if acc is None else acc
        self.pos = self.pos if pos is None else pos

    def printHistory(self):
        print('\n'.join(['(%-3d, %-4d)' % (pos, acc) for (pos, acc) in self.executedInstructions.items()]), '\n')

    def __str__(self):
        return '(%-3d, %-4d) --> isLooping? %s' % (self.pos, self.acc, self.isLooping())

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

programInstructions = [(INSTRUCTIONS[s], int(v)) for (s, v) in [l.split(' ') for l in lines]]

########
# PART 1
########

program = Program(instructions = programInstructions, acc = 0)
program.run()

#program.printHistory()

lastInstruction = next(reversed(program.executedInstructions))
lastAccumulatorValue = program.executedInstructions[lastInstruction]
print('1) Accumulator value immediately before looping program instructions: %d' % lastAccumulatorValue)

########
# PART 2
########

for i in range(0, len(programInstructions)):
    modifiedInstructions = programInstructions[:] # Copy program
    (instruction, value) = modifiedInstructions[i]

    runModifiedProgram = False
    if instruction == INSTRUCTIONS.jmp:
        modifiedInstructions[i] = (INSTRUCTIONS.nop, value)
        runModifiedProgram = True
    elif instruction == INSTRUCTIONS.nop:
        modifiedInstructions[i] = (INSTRUCTIONS.jmp, value)
        runModifiedProgram = True

    if runModifiedProgram:
        modifiedProgram = Program(instructions = modifiedInstructions, acc = 0)
        modifiedProgram.run()

        if modifiedProgram.isTerminated():
            break # Program is fixed ^_^

print('\nProgram was fixed by altering instruction #%d: %s %d\n' % (i, modifiedInstructions[i][0], modifiedInstructions[i][1]))
print('2) Fixed program terminates with accumulator value: %d' % modifiedProgram.acc)