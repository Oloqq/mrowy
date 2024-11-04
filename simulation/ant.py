from simulation.node import Node, Direction

from pygame import Vector2
import numpy as np
import random


class Ant:
    def __init__(self, position: Vector2, destination: Vector2, pheromone_flavor: int):
        self.source = position.copy()
        self.pos = position
        self.destination = destination
        self.pheromone_flavor = pheromone_flavor

    def choose_step_direction(self) -> Direction:
        TMP_EXPLORATION_CHANCE = 1.1 # TODO simulation settings
        if random.random() < TMP_EXPLORATION_CHANCE:
            return random.choice(list(Direction))
        else:
            # return max of pheromones
            raise NotImplementedError


    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        x, y = self.pos
        # FIXME Vector2 stores floats, so is useless here
        x = int(x)
        y = int(y)
        direction = self.choose_step_direction()
        dx, dy = direction.to_vector()
        dx = int(dx)
        dy = int(dy)
        current_node: Node = nodes[x][y]
        next_node: Node = nodes[x+dx][y+dy]
        if not next_node.can_move_into():
            return

        current_node.spare_capacity += 1
        next_node.spare_capacity -= 1
        assert next_node.spare_capacity >= 0

        self.deposit_pheromone(current_node, direction)
        self.pos += direction.to_vector()


    def deposit_pheromone(self, current_node: Node, direction: Direction):
        increase = 0.0 # TODO
        current_node.pheromones[self.pheromone_flavor][direction.value] += increase

    def finished(self) -> bool: # needed?
        return self.pos == self.destination
