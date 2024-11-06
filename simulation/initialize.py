from settings.simulation_settings import SimulationSettings
from settings.display_settings import DisplaySettings
from constants.enums import FieldType, ObjectType
from PIL import Image

import os
import numpy as np
import pygame as pg

def create_grid(sim_settings: SimulationSettings):
    name = "mapav4.png"
    if os.path.exists(name):
        image = Image.open(name)
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

def grid_and_objects(save_name: str, sim_settings: SimulationSettings):
    grid: np.ndarray
    objects = None

    grid = create_grid(sim_settings)

    return grid, objects

def window(sim_settings: SimulationSettings, display_settings: DisplaySettings):
    window_size = (display_settings.TILE_SIZE * sim_settings.generic.grid_size[0],
                    display_settings.TILE_SIZE * sim_settings.generic.grid_size[1])
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

    return mappedImage