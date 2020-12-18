################################
# Mapping utils for 3D problems
################################
from typing import List, Dict
from collections import namedtuple
from map2d import Coordinate, get2dAdjacentDirections

# Coordinate
Coordinate3d = namedtuple('Coordinate3d', ['x', 'y', 'z'])

# 3 ** 3 = 26 adjacent neighbors
def get3dAdjacentDirections() -> List[Coordinate3d]:
    directions2d = get2dAdjacentDirections() + [Coordinate(0, 0)]
    directions3d = [Coordinate3d(d.x, d.y, z) for d in directions2d for z in (-1, 0, 1)]
    return [d for d in directions3d if d != Coordinate3d(0, 0, 0)]

def get3dAdjacentPositions(p: Coordinate3d) -> List[Coordinate3d]:
    return [Coordinate3d(p.x + d.x, p.y + d.y, p.z + d.z) for d in get3dAdjacentDirections()]

# Distance
def get3dManhattanDistance(p1: Coordinate3d, p2: Coordinate3d) -> int:
    return abs(p2.x - p1.x) + abs(p2.y - p1.y) + abs(p2.z - p1.z)