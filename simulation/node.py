import numpy as np
from enum import Enum
from typing import assert_never
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings.simulation_settings import GenericSimulationSettings

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
    def __init__(self, available_fields: np.ndarray, neighborhood: tuple[bool, bool, bool, bool],
                 settings: "GenericSimulationSettings"):
        # neighbor order: top, right, bottom, left
        self.has_neighbor: np.ndarray = np.array(neighborhood)
        self.pheromones: dict[Coords, np.ndarray] = {}
        self.capacity = settings.node_capacity
        self.spare_capacity = self.capacity
        self.max_smell = settings.node_max_smell

        # TODO: remove this and use Grid 
        for x in range(available_fields.shape[0]):
            for y in range(available_fields.shape[1]):
                if available_fields[x][y]:
                    self.pheromones[(x, y)] = np.zeros(4)

    def can_move_into(self) -> bool:
        return self.spare_capacity > 0

    def mean_intensity(self, flavor: Pheromone, x: int, y: int, nodes: list[list["Node"]]) -> float:
        relevant_smells = []
        relevant_smells.append(
            nodes[x][y - 1].pheromones[flavor][Direction.Down.value] if self.has_neighbor[Direction.Up.value] else 0)
        relevant_smells.append(
            nodes[x + 1][y].pheromones[flavor][Direction.Left.value] if self.has_neighbor[Direction.Right.value] else 0)
        relevant_smells.append(
            nodes[x][y + 1].pheromones[flavor][Direction.Up.value] if self.has_neighbor[Direction.Down.value] else 0)
        relevant_smells.append(
            nodes[x - 1][y].pheromones[flavor][Direction.Right.value] if self.has_neighbor[Direction.Left.value] else 0)
        s = min(np.sum(relevant_smells), self.max_smell)
        return s / self.max_smell
