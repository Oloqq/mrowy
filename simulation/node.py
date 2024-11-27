import numpy as np
from enum import Enum

from typing import TYPE_CHECKING, assert_never

if TYPE_CHECKING:
    from settings.simulation_settings import GenericSimulationSettings

Coords = tuple[int, int]
Pheromone = Coords

PerColony = list
Intensity = float


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


class Node:
    def __init__(self, available_fields: np.ndarray, neighborhood: tuple[bool, bool, bool, bool],
                 settings: "GenericSimulationSettings"):
        # neighbor order: top, right, bottom, left
        self.has_neighbor: np.ndarray = np.array(neighborhood)
        self.pheromones: float
        self.capacity = settings.node_capacity
        self.spare_capacity = self.capacity
        self.max_smell = settings.node_max_smell

        # TODO: remove this and use Grid 
        for x in range(available_fields.shape[0]):
            for y in range(available_fields.shape[1]):
                if available_fields[x][y]:
                    self.pheromones = 0.0

    def can_move_into(self) -> bool:
        return self.spare_capacity > 0

    def get_pheromone_intensity(self) -> float:
        return self.pheromones / self.max_smell

    def decay_pheromones(self, decay_rate: float):
        self.pheromones = max(0.0, self.pheromones - decay_rate)
