from constants.enums import FieldType
from dataclasses import dataclass
import pygame as pg


@dataclass
class DisplaySettings:
    TILE_SIZE = 20
    field_colors = {
        FieldType.GRASS: (0, 255, 0),
        FieldType.FOREST: (0, 100, 0),
        FieldType.WATER: (0, 0, 255),
        FieldType.URBAN: (100, 100, 100)
    }
    ant_image = pg.image.load("assets/ant.png")
    colony_image = pg.image.load('assets/colony.png')
    GRID_WIDTH = 30
    GRID_HEIGHT = 50
