################################
# Mapping utils for 4D problems
################################
from typing import List, Dict
from collections import namedtuple
from map3d import Coordinate3d, get3dAdjacentDirections

# Coordinate
Coordinate4d = namedtuple('Coordinate4d', ['x', 'y', 'z', 'w'])

# 3 ** 4 = 80 adjacent neighbors
def get4dAdjacentDirections() -> List[Coordinate4d]:
    directions3d = get3dAdjacentDirections() + [Coordinate3d(0, 0, 0)]
    directions4d = [Coordinate4d(d.x, d.y, d.z, w) for d in directions3d for w in (-1, 0, 1)]
    return [d for d in directions4d if d != Coordinate4d(0, 0, 0, 0)]

def get4dAdjacentPositions(p: Coordinate4d) -> List[Coordinate4d]:
    return [Coordinate4d(p.x + d.x, p.y + d.y, p.z + d.z, p.w + d.w) for d in get4dAdjacentDirections()]

# Distance
def getManhattanDistance4d(p1: Coordinate4d, p2: Coordinate4d) -> int:
    return abs(p2.x - p1.x) + abs(p2.y - p1.y) + abs(p2.z - p1.z) + abs(p2.w - p1.w)