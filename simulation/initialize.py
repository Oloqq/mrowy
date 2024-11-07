from settings.simulation_settings import SimulationSettings
from settings.display_settings import DisplaySettings
from constants.enums import FieldType, ObjectType
from simulation.node import Node
from PIL import Image

import os
import numpy as np
import pygame as pg

def create_grid(sim_settings: SimulationSettings):
    map_img_path = sim_settings.generic.map_image_path
    if os.path.exists(map_img_path) and sim_settings.generic.create_grid_from_img:
        image = Image.open(map_img_path)
        print("image size: ", image.size)
        print(sim_settings.generic.grid_size)

        print("Loaded grid from file")
        img_array = np.asarray(image)[:,:,:3]
        assert img_array.shape[0] == sim_settings.generic.grid_size[1] # numpy uses height first
        assert img_array.shape[1] == sim_settings.generic.grid_size[0]

        print("img_array size: ", img_array.shape)

        grid = mapImageToFieldType(img_array)
    else:
        print("Created new grid")
        grid = np.full(sim_settings.generic.grid_size, FieldType.GRASS, dtype=FieldType)
    return grid

def grid_and_objects(save_name: str, sim_settings: SimulationSettings) -> tuple[np.ndarray, np.ndarray, list[list[Node]]]:
    grid: np.ndarray
    nodes: list[list[Node]] = []
    objects = None

    if os.path.exists(save_name) and not sim_settings.generic.create_grid_from_img:
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
        grid = create_grid(sim_settings)

    for x, column in enumerate(grid):
        node_column = []
        for y, val in enumerate(column):
            # TODO check tile kind
            up = y > 0 and grid[x][y-1] != FieldType.BUILDINGS
            # right = x < sim_settings.generic.grid_size[0]
            # down = y < sim_settings.generic.grid_size[1] # TODO use the whole map
            right = x < 15 and grid[x+1][y] != FieldType.BUILDINGS
            down = y < 15 and grid[x][y+1] != FieldType.BUILDINGS
            left = x > 0 and grid[x-1][y] != FieldType.BUILDINGS

            node_column.append(Node((up, right, down, left)))
        nodes.append(node_column)

    return grid, objects, nodes

def window(sim_settings: SimulationSettings):
    window_size = (sim_settings.generic.tile_size * sim_settings.generic.grid_size[0],
                    sim_settings.generic.tile_size * sim_settings.generic.grid_size[1])
    return pg.display.set_mode(window_size)


def mapImageToFieldType(image: np.ndarray):
    mappedImage = np.zeros(image[:,:,1].shape, dtype=FieldType)
    print("mapped image size: ", mappedImage.shape)
    g = 0
    p = 0
    b = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if np.array_equal(image[i, j], [255, 255, 255]):
                mappedImage[i, j] = FieldType.GRASS
                g += 1
            elif np.array_equal(image[i, j], [255, 191, 0]):
                p += 1
                mappedImage[i, j] = FieldType.PATH
            elif np.array_equal(image[i, j], [0, 0, 0]):
                mappedImage[i, j] = FieldType.BUILDINGS
                b += 1
            else:
                raise ValueError(f"Unknown color at {i}, {j}: {image[i, j]}")
    print(f"Grass: {g}, Path: {p}, Buildings: {b}")

    return mappedImage.transpose() # numpy uses height first