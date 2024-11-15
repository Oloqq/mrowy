from settings.simulation_settings import SimulationSettings
from constants.enums import FieldType
from simulation.node import Node
from PIL import Image

import os
import numpy as np
import pygame as pg


def create_grid(sim_settings: SimulationSettings):
    map_img_path = sim_settings.generic.map_image_path
    if os.path.exists(map_img_path) and sim_settings.generic.create_grid_from_img:
        image = Image.open(map_img_path)

        img_width, img_height = image.size
        sim_settings.generic.grid_size = (img_width, img_height)
        print("Updated grid size to match image dimensions:", sim_settings.generic.grid_size)

        img_array = np.asarray(image)[:, :, :3]
        # konieczne przekształcenie bo inaczej obraz jest obrócony
        img_array = img_array.transpose((1, 0, 2))
        print("Image array shape:", img_array.shape)

        assert img_array.shape[0] == sim_settings.generic.grid_size[0], \
            f"Image height ({img_array.shape[0]}) does not match grid height ({sim_settings.generic.grid_size[0]})"
        assert img_array.shape[1] == sim_settings.generic.grid_size[1], \
            f"Image width ({img_array.shape[1]}) does not match grid width ({sim_settings.generic.grid_size[1]})"

        grid = mapImageToFieldType(img_array)
    else:
        print("Creating a new grid with default settings")
        grid = np.full(sim_settings.generic.grid_size, FieldType.GRASS, dtype=FieldType)

    return grid


def grid_and_objects(save_name: str, sim_settings: SimulationSettings) -> tuple[
    np.ndarray, np.ndarray, list[list[Node]]]:
    grid: np.ndarray
    nodes: list[list[Node]] = []
    objects = None

    try:
        if os.path.exists(save_name) and not sim_settings.generic.create_grid_from_img:
            loaded_data = np.load(save_name, allow_pickle=True)
            loaded_grid = loaded_data.get('grid')
            loaded_objects = loaded_data.get('objects', np.full(sim_settings.generic.grid_size, None))

            if loaded_grid is not None and loaded_grid.shape == sim_settings.generic.grid_size:
                print("Loaded grid from file")
                grid = loaded_grid
            else:
                print("Mismatch in grid size, creating a new grid")
                grid = create_grid(sim_settings)

            if loaded_objects is not None and loaded_objects.shape == sim_settings.generic.grid_size:
                objects = loaded_objects
            else:
                objects = np.full(sim_settings.generic.grid_size, None)
        else:
            grid = create_grid(sim_settings)
            objects = np.full(sim_settings.generic.grid_size, None)
    except Exception as e:
        print(f"Error loading grid or objects: {e}")
        grid = create_grid(sim_settings)
        objects = np.full(sim_settings.generic.grid_size, None)

    # Create nodes
    available_fields = np.isin(grid, [FieldType.GRASS, FieldType.FOREST, FieldType.PATH])
    for y in range(sim_settings.generic.grid_size[0]):
        node_column = []
        for x in range(sim_settings.generic.grid_size[1]):
            up = y > 0 and available_fields[y - 1][x]
            right = x < sim_settings.generic.grid_size[1] - 1 and available_fields[y][x + 1]
            down = y < sim_settings.generic.grid_size[0] - 1 and available_fields[y + 1][x]
            left = x > 0 and available_fields[y][x - 1]

    return grid, objects, nodes


def window(sim_settings: SimulationSettings):
    window_size = (sim_settings.generic.tile_size * sim_settings.generic.grid_size[0],
                   sim_settings.generic.tile_size * sim_settings.generic.grid_size[1])
    print(f"Window size: {window_size}")
    return pg.display.set_mode(window_size)


def mapImageToFieldType(image: np.ndarray):
    mappedImage = np.zeros(image[:, :, 1].shape, dtype=FieldType)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel_color = image[i, j]

            if np.array_equal(pixel_color, [255, 255, 255]):  # White
                mappedImage[i, j] = FieldType.GRASS
            elif np.array_equal(pixel_color, [255, 191, 0]):  # Orange (Path)
                mappedImage[i, j] = FieldType.PATH
            elif np.array_equal(pixel_color, [0, 0, 0]):  # Black (Building)
                mappedImage[i, j] = FieldType.BUILDINGS
            else:
                print(f"Unknown color at ({i}, {j}): {pixel_color}, defaulting to GRASS")
                mappedImage[i, j] = FieldType.GRASS
    return mappedImage
