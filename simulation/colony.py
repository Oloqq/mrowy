from simulation.ant import Ant

from pygame import Vector2
import random

class Colony:
    counter: int = 0

    def __init__(self, position: Vector2, foods: list[Vector2]):
        assert Colony.counter == 0, "TEMP"
        self.id = Colony.counter
        Colony.counter += 1

        self.pos = position
        self.foods = foods

        self.ants: list[Ant] = [Ant(Vector2(12, 12))]

    def step(self):
        for ant in self.ants:
            ant.step()

        self.ants = [ant for ant in self.ants if ant.life > 0]
        self.ants.append(Ant(self.pos + Vector2(random.randint(1, 6), 1)))