import numpy as np
from enum import Enum
from pygame import Vector2
from typing import assert_never

class Direction(Enum):
    Up = 0,
    Right = 1,
    Down = 2,
    Left = 3

    def to_vector(self) -> Vector2:
        if self == Direction.Up:
            return Vector2(0, -1)
        elif self == Direction.Right:
            return Vector2(1, 0)
        elif self == Direction.Down:
            return Vector2(0, 1)
        elif self == Direction.Left:
            return Vector2(-1, 0)
        assert_never()

PerColony = list
Intensity = float

class Node:
    def __init__(self, neighborhood: tuple[bool, bool, bool, bool]):
        # neighbor order: top, right, bottom, left
        self.has_neighbor: np.ndarray = np.array(neighborhood)
        TMP_NUM_COLONIES = 1 # TODO set it in simulation_settings
        self.pheromones: PerColony[(Intensity, Intensity, Intensity, Intensity)] = [
            np.zeros(4) for _ in range(TMP_NUM_COLONIES)
        ]
        TMP_CAPACITY = 1 # TODO how to determine?
        self.capacity = TMP_CAPACITY
        self.spare_capacity = self.capacity

    def can_move_into(self) -> bool:
        return self.spare_capacity > 0

