from constants.enums import FieldType
from dataclasses import dataclass
import pygame as pg


@dataclass
class DisplaySettings:
    TILE_SIZE = 20
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
    GRID_WIDTH_OLD = 30
    GRID_HEIGHT_OLD = 50
    GRID_WIDTH_NEW = 273
    GRID_HEIGHT_NEW = 47
