from constants.enums import FieldType, ObjectType
from dataclasses import dataclass
import pygame as pg


@dataclass
class PygameSettings:
    TILE_SIZE = 20
    field_colors = {
        FieldType.GRASS: (0, 255, 0),
        FieldType.FOREST: (0, 100, 0),
        FieldType.WATER: (0, 0, 255),
        FieldType.URBAN: (100, 100, 100)
    }
    object_images = {
        ObjectType.HUNTER: pg.image.load('assets/hunter.png'),
        ObjectType.FOX_DEN: pg.image.load('assets/fox_den.png'),
        ObjectType.RABBIT_DEN: pg.image.load('assets/rabbit_den.png')
    }
    FOX_IMAGE = pg.image.load("assets/fox.png") #did not see it anywhere else so I added it here
    SAVE_NAME = "grid.npz"
    GRID_WIDTH = 30
    GRID_HEIGHT = 50


def get_default_pygame_settings() -> PygameSettings:
    return PygameSettings()
