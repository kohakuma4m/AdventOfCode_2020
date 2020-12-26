import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

REMINDER_VALUE = 20201227

def getNextValue(value: int, subjectNumber: int) -> int:
    return (value * subjectNumber) % REMINDER_VALUE

def transformSubjectNumber(loopSize: int, subjectNumber: int) -> int:
    value = 1
    for _ in range(loopSize):
        value = getNextValue(value, subjectNumber)

    return value

INITIAL_SUBJECT_NUMBER = 7

def generatePublicKey(loopSize: int) -> int:
    return transformSubjectNumber(loopSize, subjectNumber=INITIAL_SUBJECT_NUMBER)

def generateEncryptionKey(loopSize: int, publicKey: int) -> int:
    return transformSubjectNumber(loopSize, subjectNumber=publicKey)

def findLoopSize(publicKey: int) -> int:
    loopSize = 1
    value = getNextValue(value=1, subjectNumber=INITIAL_SUBJECT_NUMBER)
    while value != publicKey:
        loopSize += 1
        value = getNextValue(value, subjectNumber=INITIAL_SUBJECT_NUMBER)

    return loopSize

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

cardPublicKey = int(lines[0])
doorPublicKey = int(lines[1])

########
# PART 1
########

print('--------------------------')
print('Card public key: %d' % cardPublicKey)
print('Door public key: %d' % doorPublicKey)
print('--------------------------\n')

print('Finding card loop size...')
cardLoopSize = findLoopSize(cardPublicKey)
print('Card loop size: %d\n' % cardLoopSize)

print('Finding card encryption key using door public key...')
cardEncryptionKey = generateEncryptionKey(cardLoopSize, doorPublicKey)
print('1) The encryption key for card-door handshaking: %d\n' % cardEncryptionKey)