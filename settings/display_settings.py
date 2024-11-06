from constants.enums import FieldType
from dataclasses import dataclass
import pygame as pg


@dataclass
class DisplaySettings:
    TILE_SIZE = 7
    field_colors = {
        FieldType.GRASS: (255, 255, 255),
        FieldType.PATH: (255, 191, 0),
        FieldType.BUILDINGS: (0, 0, 0)
    }
    ant_image = pg.image.load("assets/ant.png")
    colony_image = pg.image.load('assets/colony.png')
    GRID_WIDTH = 273
    GRID_HEIGHT = 47
