from settings.simulation_settings import SimulationSettings
from settings.display_settings import DisplaySettings
from constants.enums import FieldType, ObjectType
from simulation.node import Node

import os
import numpy as np
import pygame as pg

def grid_and_objects(save_name: str, sim_settings: SimulationSettings) -> tuple[np.ndarray, np.ndarray, list[list[Node]]]:
    grid: np.ndarray
    nodes: list[list[Node]] = []
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
        raise NotImplementedError
        # FIXME tworzenie od zera nie działa
        # print("Created new grid")
        # grid = np.full(sim_settings.generic.grid_size, FieldType.GRASS, dtype=FieldType)
        # objects = np.full(sim_settings.generic.grid_size, ObjectType.NOTHING, dtype=ObjectType)

    for x, column in enumerate(grid):
        node_column = []
        for y, val in enumerate(column):
            # TODO check tile kind
            up = y > 0 and grid[x][y-1] != FieldType.WATER
            # right = x < sim_settings.generic.grid_size[0]
            # down = y < sim_settings.generic.grid_size[1] # FIXME sim_settings grid size does not match reality (those lines casue index error)
            right = x < 5 and grid[x+1][y] != FieldType.WATER
            # print(down)
            down = y < 15 and grid[x][y+1] != FieldType.WATER
            left = x > 0 and grid[x-1][y] != FieldType.WATER

            node_column.append(Node((up, right, down, left)))
        nodes.append(node_column)

    return grid, objects, nodes

def window(sim_settings: SimulationSettings, display_settings: DisplaySettings):
    window_size = (display_settings.TILE_SIZE * sim_settings.generic.grid_size[0],
                    display_settings.TILE_SIZE * sim_settings.generic.grid_size[1])
    return pg.display.set_mode(window_size)