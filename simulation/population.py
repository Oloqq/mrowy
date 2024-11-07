from simulation.ant import Ant
from simulation.node import Node

from pygame import Vector2
import numpy as np
import random

class Population:
    def __init__(self):
        self.spawn_interval = 30 # TODO settings
        self.time_to_spawn = 0
        self.ants: list[Ant] = []
        self.foods = [Vector2(7, 7)] # just visual, to be removed

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        assert len(self.foods) == 1

        self.time_to_spawn -= 1

        if self.time_to_spawn <= 0 or len(self.ants) == 0:
            self.ants = []

            self.time_to_spawn = self.spawn_interval
            print("next generation")

            for _ in range(5):
                self.ants.append(
                    Ant(
                        position=(7, 7),
                        destination=(random.randint(0, 14), random.randint(0, 14)),
                    )
                )

            for _ in range(3):
                self.ants.append(
                    Ant(
                        position=(random.randint(0, 14), random.randint(0, 14)),
                        destination=(7, 7),
                    )
                )

            # TEMP restriction, also in initialize.grid
            # for x in range(15):
            #     for y in range(15):
            #         if random.random() < 0.5:
            #             continue
            #         goalx = random.randint(0, 14)
            #         goaly = random.randint(0, 14)
            #         if x == goalx and y == goaly:
            #             continue

            #         self.ants.append(
            #         Ant(
            #             position=(int(x), int(y)),
            #             destination=(int(goalx), int(goaly)),
            #         )
            #     )
            # randi = random.randint(0, len(self.ants) - 1)
            # replace = self.ants[randi]
            # self.ants[randi] = Ant(position=replace.pos, destination=(7, 7))


        for ant in self.ants:
            ant.step(grid, objects, nodes)

        self.ants = [ant for ant in self.ants if not ant.ready_to_die]