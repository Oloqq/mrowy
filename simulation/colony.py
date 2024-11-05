from simulation.ant import Ant
from simulation.node import Node

from pygame import Vector2
import numpy as np

class Colony:
    counter: int = 0

    def __init__(self, position: Vector2, foods: list[Vector2]):
        assert Colony.counter == 0, "TEMP"
        self.id = Colony.counter
        Colony.counter += 1

        self.pos = position
        self.foods = foods

        self.ants: list[Ant] = []

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        assert len(self.foods) == 1
        while len(self.ants) < 2:
            self.ants.append(
                Ant(
                    position=Vector2(self.pos.x, self.pos.y),
                    destination=Vector2(self.foods[0].x, self.foods[0].y),
                    pheromone_flavor=self.id
                )
            )

        for ant in self.ants:
            ant.step(grid, objects, nodes)

        self.ants = [ant for ant in self.ants if not ant.finished()]