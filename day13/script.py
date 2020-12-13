import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

def findEarliestNextBus(earliestTimestamp: int, busIds: list) -> (int, int):
    # Schedule of bus that passed just before earliest timestamp
    busSchedule = { id: id * (earliestTimestamp // id) for id in busIds }

    while True:
        busSchedule = { busId: timestamp + busId for busId, timestamp in busSchedule.items() }
        nextBusId = min(busSchedule.keys(), key=lambda busId: busSchedule[busId])
        if busSchedule[nextBusId] > earliestTimestamp:
            return (nextBusId, busSchedule[nextBusId])

def findEarliestSynchronizedTimestamp(busIds: list, busOffsets: dict) -> int:
    time = 0
    previousBusPeriod = busIds[0] # Previous bus pass once each X minutes
    for i in range(1, len(busIds)):
        nextBus = busIds[i] # Next bus pass once each Y minutes

        # Until next bus is A minutes afer current bus (i.e: when schedule align with next bus period)
        while (time + busOffsets[nextBus]) % nextBus != 0:
            time += previousBusPeriod # Going to next time previous bus will pass, X minutes later

        # We treat all synchronized bus as one big bus with combined synced period
        previousBusPeriod *= nextBus # Synced bus pass once each X = X * Y minutes

    return time

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

earliestTimestamp = int(lines[0])

allBus = [x for x in lines[1].split(',')]
busIds = [int(id) for id in allBus if id != 'x']
nbRunningBus = len(busIds)

########
# PART 1
########

# Finding earliest next bus
(nextBusId, nextTimestamp) = findEarliestNextBus(earliestTimestamp, busIds)

waitingTime = nextTimestamp - earliestTimestamp
product = nextBusId * waitingTime
print(f'Start waiting at {earliestTimestamp} for next bus among {nbRunningBus} running bus')
print(f'The earliest next bus is at timestamp {nextTimestamp}, in {waitingTime} minutes\n')
print(f'1) Product = {nextBusId} * {waitingTime} = {product}\n')

########
# PART 2
########

# Full list of bus by offset
busOffsets = { int(allBus[i]): i for i in range(0, len(allBus)) if allBus[i] != 'x'}

earliestSynchronizedTimestamp = findEarliestSynchronizedTimestamp(busIds, busOffsets)
print(f'2) Earliest timestamp at wich all running bus are synchronized is {earliestSynchronizedTimestamp}\n')