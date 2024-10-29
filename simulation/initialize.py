from settings.simulation_settings import SimulationSettings
from settings.display_settings import DisplaySettings
from constants.enums import FieldType, ObjectType, DayPart, Sex

import os
import numpy as np
import pygame as pg

def grid_and_objects(save_name: str, sim_settings: SimulationSettings):
    grid: np.ndarray
    objects = None
    if os.path.exists(save_name):
        loaded_data = np.load(save_name, allow_pickle=True)
        loaded_grid = loaded_data['grid']
        loaded_objects = loaded_data['objects']
        if (loaded_grid.shape == sim_settings.generic.grid_size and
                loaded_objects.shape == sim_settings.generic.grid_size):
            print("Loaded grid from file")
            grid = loaded_grid
            objects = loaded_objects
        elif loaded_grid.shape != sim_settings.generic.grid_size:
            raise ValueError(f"Grid size in file does not match simulation settings\n"
                                f"Grid size in file: {loaded_grid.shape}\n"
                                f"Expected grid size: {sim_settings.generic.grid_size}")
        else:
            raise ValueError(f"Object grid size in file does not match simulation settings\n"
                                f"Grid size in file: {loaded_objects.shape}\n"
                                f"Expected grid size: {sim_settings.generic.grid_size}")
    else:
        # FIXME tworzenie od zera nie działa
        print("Created new grid")
        grid = np.full(sim_settings.generic.grid_size, FieldType.GRASS, dtype=FieldType)
        objects = np.full(sim_settings.generic.grid_size, ObjectType.NOTHING, dtype=ObjectType)

    rabbits_in_dens = {}
    yy, xx = objects.shape
    for y in range(yy):
        for x in range(xx):
            if objects[y, x] == ObjectType.RABBIT_DEN:
                rabbits_in_dens[(y, x)] = 15

    return grid, objects, rabbits_in_dens

def window(sim_settings: SimulationSettings, display_settings: DisplaySettings):
    window_size = (display_settings.TILE_SIZE * sim_settings.generic.grid_size[0],
                    display_settings.TILE_SIZE * sim_settings.generic.grid_size[1])
    return pg.display.set_mode(window_size)

# def simulation(objects, sim_settings: SimulationSettings):
#     fox_dens = np.where(self.objects == ObjectType.FOX_DEN)
#     self.population_manager.create_population(list(zip(*fox_dens)), self.time_manager.date)
#     self.home_ranges = np.full(sim_settings.generic.grid_size, 0, dtype=object)

#     for fox in self.population_manager.get_foxes():
#         for pos in fox.home_range:
#             if 0 <= pos[0] < sim_settings.generic.grid_size[0] and \
#                     0 <= pos[1] < sim_settings.generic.grid_size[1]:
#                 self.home_ranges[pos] = 1