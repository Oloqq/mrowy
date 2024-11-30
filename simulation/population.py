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

            minimum_shortest_path_to_destination = self.sim_settings.population.ant_max_memory
            new_ants = []

            if len(self.ants) > 0:
                for ant in self.ants:
                    if ant.is_returning and len(ant.visited_fields_copy) < minimum_shortest_path_to_destination:
                        minimum_shortest_path_to_destination = len(ant.visited_fields_copy)

                for ant in self.ants:
                    if ant.is_returning and len(ant.visited_fields_copy) < 1.2 * minimum_shortest_path_to_destination:
                        new_ants.append(ant)

            self.ants = new_ants
            print(str(len(self.ants))
                  + " ants had path shorter than 1.25 * minimum_shortest_path_to_destination. Minimum shortest path: "
                  + str(minimum_shortest_path_to_destination))

            self.time_to_spawn = self.spawn_interval
            print("next generation: adding new ants of number: "
                  + str(self.sim_settings.population.population_size - len(self.ants)))

            for _ in range(self.sim_settings.population.population_size - len(self.ants)):
                self.ants.append(
                    Ant(
                        position=self.sim_settings.generic.source,
                        destination=self.sim_settings.generic.target,
                        destination_bonus=self.sim_settings.population.destination_bonus,
                        max_memory=self.sim_settings.population.ant_max_memory
                    )
                )

        for ant in self.ants:
            ant.step(grid, objects, nodes)

        self.ants = [ant for ant in self.ants if not ant.ready_to_die]
