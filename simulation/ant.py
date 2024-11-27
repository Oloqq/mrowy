from collections import OrderedDict
import numpy as np
import random
from simulation.node import Node, Coords, Direction


class Ant:
    def __init__(self, position: Coords, destination: Coords, destination_bonus: float):
        self.is_returning = False
        self.source = position
        self.pos = position
        self.destination = destination
        self.age = 0
        self.ready_to_die = False
        self.color = (255, 0, 0)
        self.visited_fields = OrderedDict()
        self.visited_fields[position] = None
        self.max_memory = 500
        self.previous_field = None
        self.exploration_chance = 0.2
        self.destination_bonus = destination_bonus

        self.visited_fields_copy = None
        self.bonus = 0.0
        self.next_field = None
        self.previous_direction = None

    def add_to_visited(self, position: tuple[int, int]):
        if position in self.visited_fields:
            # If the position already exists, remove and re-add it to maintain order
            del self.visited_fields[position]
        elif len(self.visited_fields) >= self.max_memory:
            self.visited_fields.popitem(last=False)  # Remove first item (FIFO)

        self.visited_fields[position] = None  # Add the position as the newest entry

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        self.age += 1
        x, y = self.pos
        current_node: Node = nodes[x][y]
        if self.is_returning:
            if self.pos == self.destination:
                self.source, self.destination = self.destination, self.source
                self.is_returning = True
                # reverse the visited fields copy
                self.visited_fields_copy = OrderedDict(reversed(self.visited_fields_copy.items()))
                self.visited_fields = self.visited_fields_copy.copy()

            if not self.visited_fields:
                # should not happen
                self.source, self.destination = self.destination, self.source
                self.is_returning = False
                self.bonus = 0.0
                self.ready_to_die = True
                print("Ant died.")
                return
            # Get the last visited field and remove it
            next_field = list(reversed(self.visited_fields.keys()))[0]
            del self.visited_fields[next_field]

            self.pos = next_field
            dx, dy = next_field[0] - x, next_field[1] - y
            self.transfer(fromnode=current_node, tonode=nodes[x + dx][y + dy])

        else:
            direction = self.choose_step_direction(current_node, nodes, x, y)
            dx, dy = direction.to_vector()
            next_x, next_y = x + dx, y + dy

            if (next_x, next_y) == self.previous_field:
                direction = self.explore(nodes)
                dx, dy = direction.to_vector()
                next_x, next_y = x + dx, y + dy

            if 0 <= next_x < len(nodes) and 0 <= next_y < len(nodes[0]):
                next_node: Node = nodes[next_x][next_y]

                if current_node.has_neighbor[direction.value]:
                    self.previous_field = self.pos
                    self.pos = (next_x, next_y)
                    self.transfer(fromnode=current_node, tonode=next_node)
                    self.add_to_visited(self.pos)

                    if self.pos == self.destination:
                        self.source, self.destination = self.destination, self.source

                        self.is_returning = True
                        self.bonus = self.destination_bonus
                        self.visited_fields_copy = self.visited_fields.copy()

    def choose_step_direction(self, from_node: Node, nodes: list[list[Node]], current_x: int,
                              current_y: int) -> Direction:
        pheromone_values = [0] * 4
        for i in range(4):
            if not from_node.has_neighbor[i]:
                pheromone_values[i] = 0
            else:
                dx, dy = Direction(i).to_vector()
                neighbor_x, neighbor_y = current_x + dx, current_y + dy

                if 0 <= neighbor_x < len(nodes) and 0 <= neighbor_y < len(nodes[0]):
                    neighbor = nodes[neighbor_x][neighbor_y]
                    pheromone_values[i] = neighbor.pheromones

        if random.random() < self.exploration_chance or max(pheromone_values) < 40:
            return self.explore(nodes)
        else:
            return Direction(np.argmax(pheromone_values))

    def explore(self, nodes: list[list[Node]]) -> Direction:
        x, y = self.pos
        limit = 20
        while limit > 0:
            random_direction = random.choice(list(Direction))
            dx, dy = random_direction.to_vector()
            new_x, new_y = x + dx, y + dy

            if (new_x, new_y) != self.previous_field and nodes[x][y].has_neighbor[random_direction.value]:
                return random_direction

            limit -= 1
        return random.choice(list(Direction))

    def transfer(self, fromnode: Node, tonode: Node):
        fromnode.spare_capacity += 1
        tonode.spare_capacity -= 1
        delta = self.pheromone_deposited()
        self.deposit_pheromone(fromnode, delta)

    def deposit_pheromone(self, node: Node, delta: float = 1.0):
        if node is not None:
            pheromone_values = node.pheromones

            # Apply bonus pheromone when returning
            deposit_value = delta + (self.bonus if self.is_returning else 0)
            pheromone_values = min(pheromone_values + deposit_value, node.max_smell)
            node.pheromones = pheromone_values
            print(pheromone_values)

    def pheromone_deposited(self) -> float:
        delta_tau = 5 / np.sqrt(self.age)
        return delta_tau
