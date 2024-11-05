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
        self.travel_time = 0

    def choose_step_direction(self, from_node: Node) -> Direction:
        def explore():
            return random.choice(list(Direction))

        TMP_EXPLORATION_CHANCE = 0.1 # TODO simulation settings
        if random.random() < TMP_EXPLORATION_CHANCE:
            return explore()
        else:
            relevant_smells = from_node.pheromones[self.pheromone_flavor] * from_node.has_neighbor
            # edge case of initial exploration when all pheromones are 0
            if (relevant_smells == 0).all():
                return explore()
            return Direction(relevant_smells.argmax())

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        self.travel_time += 1

        x, y = self.pos
        # FIXME Vector2 stores floats, so is useless here
        x = int(x)
        y = int(y)
        current_node: Node = nodes[x][y]
        direction = self.choose_step_direction(current_node)
        dx, dy = direction.to_vector()
        dx = int(dx)
        dy = int(dy)
        next_node: Node = nodes[x+dx][y+dy]

        # ants can occasionally get stuck (for a single step) if they try to explore in an inpassable direction
        # NOTE if a node has no capacity, the ant will just wait, is it ok?
        if next_node.spare_capacity > 0 and current_node.has_neighbor[direction.value]:
            self.pos += direction.to_vector()
            self.transfer(source=current_node, direction=direction, to=next_node)

    def transfer(self, source: Node, direction: Direction, to: Node):
        source.spare_capacity += 1
        assert to.spare_capacity > 0
        to.spare_capacity -= 1
        self.deposit_pheromone(source, direction)


    def deposit_pheromone(self, current_node: Node, direction: Direction):
        # pheromone amount is represented as tau (τ) in the article
        # calculating ∆τ is just described as a function of ant age so I'm improvising
        delta_tau = 1 / self.travel_time
        current_node.pheromones[self.pheromone_flavor][direction.value] += delta_tau

    def finished(self) -> bool: # needed?
        return self.pos == self.destination
