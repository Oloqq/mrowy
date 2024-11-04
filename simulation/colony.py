from simulation.ant import Ant

from pygame import Vector2

class Colony:
    counter: int = 0

    def __init__(self, position: Vector2, foods: list[Vector2]):
        assert Colony.counter == 0, "TEMP"
        self.id = Colony.counter
        Colony.counter += 1

        self.pos = position
        self.foods = foods

        self.ants: list[Ant] = []

    def step(self):
        # TEMP: keep one ant alive
        assert len(self.ants) <= 1
        assert len(self.foods) == 1
        if len(self.ants) == 0:
            self.ants.append(Ant(Vector2(self.pos.x, self.pos.y)))

        for ant in self.ants:
            ant.step()