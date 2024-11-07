import numpy as np
from enum import Enum
from typing import assert_never

Coords = tuple[int, int]
Pheromone = Coords

class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

    def to_vector(self) -> Coords:
        if self == Direction.Up:
            return (0, -1)
        elif self == Direction.Right:
            return (1, 0)
        elif self == Direction.Down:
            return (0, 1)
        elif self == Direction.Left:
            return (-1, 0)
        assert_never()

    def opposite(self) -> "Direction":
        if self == Direction.Up:
            return Direction.Down
        elif self == Direction.Right:
            return Direction.Left
        elif self == Direction.Down:
            return Direction.Up
        elif self == Direction.Left:
            return Direction.Right

PerColony = list
Intensity = float

class Node:
    def __init__(self, neighborhood: tuple[bool, bool, bool, bool]):
        # neighbor order: top, right, bottom, left
        self.has_neighbor: np.ndarray = np.array(neighborhood)
        self.pheromones: dict[Coords, np.ndarray] = {}
        for x in range(15): # TEMP
            for y in range(15):
                self.pheromones[(x, y)] = np.zeros(4)

        TMP_CAPACITY = 1 # TODO how to determine?
        self.capacity = TMP_CAPACITY
        self.spare_capacity = self.capacity

    def can_move_into(self) -> bool:
        return self.spare_capacity > 0

    def mean_intensity(self, flavor: Pheromone, x: int, y: int, nodes: list[list["Node"]]) -> float:
        TMP_MAX_SMELL = 4 # TODO how to determine
        relevant_smells = []
        relevant_smells.append(nodes[x][y-1].pheromones[flavor][Direction.Down.value] if self.has_neighbor[Direction.Up.value] else 0)
        relevant_smells.append(nodes[x+1][y].pheromones[flavor][Direction.Left.value] if self.has_neighbor[Direction.Right.value] else 0)
        relevant_smells.append(nodes[x][y+1].pheromones[flavor][Direction.Up.value] if self.has_neighbor[Direction.Down.value] else 0)
        relevant_smells.append(nodes[x-1][y].pheromones[flavor][Direction.Right.value] if self.has_neighbor[Direction.Left.value] else 0)
        s = min(np.sum(relevant_smells), TMP_MAX_SMELL)
        return s / TMP_MAX_SMELL