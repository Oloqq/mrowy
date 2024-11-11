from constants.enums import FieldType
from dataclasses import dataclass
import pygame as pg


@dataclass
class DisplaySettings:
    field_colors = {
        FieldType.PATH: (255, 191, 0),
        FieldType.BUILDINGS: (0, 0, 0),
        FieldType.GRASS: (0, 255, 0),
        FieldType.FOREST: (0, 100, 0),
        FieldType.WATER: (0, 0, 255),
        FieldType.URBAN: (100, 100, 100)
    }
    ant_image = pg.image.load("assets/ant.png")
    colony_image = pg.image.load("assets/colony.png")
    food_image = pg.image.load("assets/food.png")
    # read frid from ant.npz
    GRID_WIDTH_OLD = 30
    GRID_HEIGHT_OLD = 50
    TILE_SIZE_OLD = 20

    # new map
    GRID_WIDTH_NEW = 273
    GRID_HEIGHT_NEW = 47
    TILE_SIZE_NEW = 7

    MAX_FPS: int = 60
