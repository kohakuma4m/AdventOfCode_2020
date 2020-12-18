import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error
import map2d as mapUtils # pylint: disable=import-error
from map2d import Coordinate # pylint: disable=import-error

from enum import Enum

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON
# endregion COMMON
###########################

class ACTION(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    LEFT = 'L'
    RIGHT = 'R'
    FORWARD = 'F'

DIRECTION = {
    ACTION.NORTH: Coordinate(0, 1),
    ACTION.SOUTH: Coordinate(0, -1),
    ACTION.EAST: Coordinate(1, 0),
    ACTION.WEST: Coordinate(-1, 0)
}

ROTATION = {
    ACTION.LEFT: {
        ACTION.NORTH: ACTION.WEST,
        ACTION.SOUTH: ACTION.EAST,
        ACTION.EAST: ACTION.NORTH,
        ACTION.WEST: ACTION.SOUTH
    },
    ACTION.RIGHT: {
        ACTION.NORTH: ACTION.EAST,
        ACTION.SOUTH: ACTION.WEST,
        ACTION.EAST: ACTION.SOUTH,
        ACTION.WEST: ACTION.NORTH
    }
}

def getNbTurns(angle: int) -> int:
    return int(angle / 90) % 4

def moveShip(instructions: list, startingPosition: Coordinate, startingDirection: ACTION) -> (Coordinate, ACTION):
    position = Coordinate(startingPosition.x, startingPosition.y)
    direction = startingDirection

    for action, value in instructions:
        if action in DIRECTION:
            # Move ship position, but keep direction the same
            d = DIRECTION[action]
            position = Coordinate(position.x + value * d.x, position.y + value * d.y)
        elif action in ROTATION:
            # Rotate ship
            for _ in range(getNbTurns(value)):
                direction = ROTATION[action][direction]
        elif action == ACTION.FORWARD:
            # Move ship position in direction
            d = DIRECTION[direction]
            position = Coordinate(position.x + value * d.x, position.y + value * d.y)
        else:
            print(action)
            raise Exception('Unknown action !')

    return (position, direction)

def rotatePosition(p: Coordinate, r: ROTATION):
    if r == ACTION.RIGHT: # Clockwise
        return Coordinate(p.y, -p.x)
    else: # Counterclockwise
        return Coordinate(-p.y, p.x)

def moveShipWithWaypoint(instructions: list, shipPosition: Coordinate, wayPointPosition: Coordinate) -> (Coordinate, Coordinate, ACTION):
    currentShipPosition = Coordinate(shipPosition.x, shipPosition.y)
    currentWaypointPosition = Coordinate(wayPointPosition.x, wayPointPosition.y)

    for action, value in instructions:
        if action in DIRECTION:
            # Move waypoint only
            d = DIRECTION[action]
            currentWaypointPosition = Coordinate(currentWaypointPosition.x + value * d.x, currentWaypointPosition.y + value * d.y)
        elif action in ROTATION:
            # Move waypoint only
            for _ in range(getNbTurns(value)):
                currentWaypointPosition = rotatePosition(currentWaypointPosition, action)
        elif action == ACTION.FORWARD:
            # Move ship towards waypoint (movement amplified by waypoint)
            currentShipPosition = Coordinate(currentShipPosition.x + value * currentWaypointPosition.x, currentShipPosition.y + value * currentWaypointPosition.y)
        else:
            print(action)
            raise Exception('Unknown action !')

    return (currentShipPosition, currentWaypointPosition, direction)

###########################
# FETCH DATA
###########################
lines = utils.readFileLines(filename)

instructions = [(ACTION(s[0]), int(s[1:])) for s in lines]

########
# PART 1
########

startPosition = Coordinate(0, 0)
(endPosition, direction) = moveShip(instructions, startPosition, ACTION.EAST)
distance = mapUtils.get2dManhattanDistance(startPosition, endPosition)

print(f'1) The ship goes from ({startPosition.x}, {startPosition.y}) to ({endPosition.x}, {endPosition.y}) at distance {distance}, facing {direction.name}\n')

########
# PART 2
########

shipPosition = Coordinate(0, 0)
waypointPosition = Coordinate(10, 1)
(endShipPosition, endWaypointPosition, direction2) = moveShipWithWaypoint(instructions, shipPosition, waypointPosition)
distance2 = mapUtils.get2dManhattanDistance(shipPosition, endShipPosition)

print(f'2) The ship goes to position ({endShipPosition.x}, {endShipPosition.y}), with waypoint at ({endWaypointPosition.x}, {endPosition.y}), at distance {distance2}, facing {direction2.name}\n')