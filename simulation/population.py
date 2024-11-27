from simulation.ant import Ant
from simulation.node import Node
from settings.simulation_settings import SimulationSettings

from pygame import Vector2
import numpy as np
import random


class Population:
    def __init__(self, sim_settings: SimulationSettings):
        self.sim_settings = sim_settings
        self.spawn_interval = sim_settings.population.spawn_interval
        self.time_to_spawn = sim_settings.population.spawn_interval
        self.ants: list[Ant] = []
        self.foods = [Vector2(7, 7)]  # just visual, to be removed

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        assert len(self.foods) == 1

        self.time_to_spawn -= 1
        if self.time_to_spawn <= 0 or len(self.ants) == 0 or len(self.ants) < 0:


            self.ants = []

            self.time_to_spawn = self.spawn_interval
            print("next generation")

            for _ in range(self.sim_settings.population.population_size):
                self.ants.append(
                    Ant(
                        position=self.sim_settings.generic.source,
                        destination=self.sim_settings.generic.target,
                        destination_bonus=self.sim_settings.population.destination_bonus
                    )
                )

        for ant in self.ants:
            ant.step(grid, objects, nodes)

        self.ants = [ant for ant in self.ants if not ant.ready_to_die]
