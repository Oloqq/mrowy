from simulation.node import Node, Direction, Coords, Pheromone

import numpy as np
import random

class Ant:
    def __init__(self, position: Coords, destination: Coords):
        self.source = position
        self.pos = position
        self.destination = destination
        self.age = 0
        self.ready_to_die = False
        # self.color = (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255))
        # self.color = (0, 0, 0)
        # if self.source == (7, 7):
        self.color = (255, 0, 0)
        # elif self.destination == (7, 7):
        #     self.color = (0, 0, 255)

    def choose_step_direction(self, from_node: Node, nodes: list[list[Node]], current_x: int, current_y: int) -> Direction:
        TMP_EXPLORATION_CHANCE = 0.3 # TODO simulation settings
        # if random.random() < TMP_EXPLORATION_CHANCE and self.destination != (7, 7):
        if random.random() < TMP_EXPLORATION_CHANCE and self.destination != self.source:
            return self.explore(nodes)
        else:
            relevant_smells = from_node.pheromones[self.destination] * from_node.has_neighbor
            # edge case of initial exploration when all pheromones are 0
            if (relevant_smells == 0).all():
                return self.explore(nodes)
            if self.destination == self.source:
                print("not exploring")
            return Direction(relevant_smells.argmax())


    def explore(self, nodes: list[list[Node]]) -> Direction:
        x, y = self.pos
        limit = 20

        random_direction = random.choice(list(Direction))
        while not nodes[x][y].has_neighbor[random_direction.value] and limit > 0:
            random_direction = random.choice(list(Direction))
            limit -= 1
        return random_direction

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        self.age += 1

        x, y = self.pos
        current_node: Node = nodes[x][y]
        direction = self.choose_step_direction(current_node, nodes, x, y)
        dx, dy = direction.to_vector()
        next_node: Node = nodes[x + dx][y + dy]

        # ants can occasionally get stuck (for a single step) if they try to explore in an inpassable direction
        # NOTE if a node has no capacity, the ant will just wait, is it ok?
        # if next_node.spare_capacity > 0 and current_node.has_neighbor[direction.value]:
        if current_node.has_neighbor[direction.value]:
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
            self.transfer(fromnode=current_node, direction=direction, tonode=next_node)
            if self.pos == self.destination:
                self.ready_to_die = True

    def transfer(self, fromnode: Node, direction: Direction, tonode: Node):
        fromnode.spare_capacity += 1
        # assert to.spare_capacity > 0
        tonode.spare_capacity -= 1

        delta = self.pheromone_deposited()
        self.deposit_pheromone(tonode, self.pos, delta)
        self.decay_pheromones(tonode, delta)

    def deposit_pheromone(self, node: Node, current_pos: tuple[int, int], delta: float = 1.0):
        x, y = current_pos

        if node is not None and (x, y) in node.pheromones:
            # Add pheromone in all directions
            for direction in range(4):  # 4 directions: up, right, down, left
                current_value = node.pheromones[(x, y)][direction]
                # Increase pheromone value, but don't exceed max_smell
                node.pheromones[(x, y)][direction] = min(
                    current_value + delta,
                    node.max_smell
                )

    def pheromone_deposited(self) -> float:
        # pheromone amount is represented as tau (τ) in the article
        # calculating ∆τ is just described as a function of ant age so I'm improvising
        delta_tau = 1 / np.sqrt(self.age)
        return delta_tau

    def decay_pheromones(self, node: Node, delta: float):
        node.pheromones[self.source] /= (1 + delta)