from settings import get_default_settings
from dataclasses import dataclass
from enum import Enum
import pygame as pg
import numpy as np
import os



class FieldType(Enum):
    GRASS = 0
    FOREST = 1
    WATER = 2
    URBAN = 3

class ObjectType(Enum):
    NOTHING = 0
    HUNTER = 1
    FOX_DEN = 2
    RABBIT_DEN = 3

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
    # For quick testing on different savefiles
    SAVE_NAME = "grid.npz"

    GRID_WIDTH = 30
    GRID_HEIGHT = 50


class PygameSimulationTest:
    FPS = 30

    def __init__(self):
        self.sim_settings = get_default_settings()
        self.pg_settings = PygameSettings()
        self.sim_settings.generic.grid_size = (PygameSettings.GRID_WIDTH, PygameSettings.GRID_HEIGHT)

        # GRID AND OBJECTS INITIALIZATION
        if os.path.exists(PygameSettings.SAVE_NAME):
            loaded_data = np.load(PygameSettings.SAVE_NAME, allow_pickle=True)
            loaded_grid = loaded_data['grid']
            loaded_objects = loaded_data['objects']
            if loaded_grid.shape == self.sim_settings.generic.grid_size and loaded_objects.shape == self.sim_settings.generic.grid_size:
                print("Loaded grid from file")
                self.grid = loaded_grid
                self.objects = loaded_objects
            elif loaded_grid.shape != self.sim_settings.generic.grid_size:
                raise ValueError(f"Grid size in file does not match simulation settings\nGrid size in file: {loaded_grid.shape}\nExpected grid size: {self.sim_settings.generic.grid_size}")
            else:
                raise ValueError(f"Object grid size in file does not match simulation settings\nGrid size in file: {loaded_objects.shape}\nExpected grid size: {self.sim_settings.generic.grid_size}")

        else:
            print("Created new grid")
            self.grid = np.full(self.sim_settings.generic.grid_size, FieldType.GRASS, dtype=FieldType)
            self.objects = np.full(self.sim_settings.generic.grid_size, ObjectType.NOTHING, dtype=ObjectType)

        self.selected_tile_type = FieldType.FOREST
        self.draw_mode = True

        pg.init()
        self.screen = self.create_window()
        self.clock = pg.time.Clock()
        self.done = False

    def create_window(self):
        window_size = (PygameSettings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                       PygameSettings.TILE_SIZE * self.sim_settings.generic.grid_size[1])
        return pg.display.set_mode(window_size)

    def run(self):
        while not self.done:
            self.clock.tick(self.FPS)
            self.handle_events()
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                elif event.key == pg.K_SPACE:
                    self.draw_mode = not self.draw_mode
                elif event.key == pg.K_1:
                    self.selected_tile_type = FieldType.GRASS
                    print("Selected grass")
                elif event.key == pg.K_2:
                    self.selected_tile_type = FieldType.FOREST
                    print("Selected forest")
                elif event.key == pg.K_3:
                    self.selected_tile_type = FieldType.WATER
                    print("Selected water")
                elif event.key == pg.K_4:
                    self.selected_tile_type = FieldType.URBAN
                    print("Selected urban")
                elif event.key == pg.K_5:
                    self.selected_tile_type = ObjectType.HUNTER
                    print("Selected hunter")
                elif event.key == pg.K_6:
                    self.selected_tile_type = ObjectType.FOX_DEN
                    print("Selected fox den")
                elif event.key == pg.K_7:
                    self.selected_tile_type = ObjectType.RABBIT_DEN
                    print("Selected rabbit den")
                elif event.key == pg.K_8:
                    self.selected_tile_type = ObjectType.NOTHING
                    print("Selected object eraser")
                elif event.key == pg.K_s:
                    np.savez(PygameSettings.SAVE_NAME, grid=self.grid, objects=self.objects)
                    print("Saved grid to file")
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.draw_mode:
                    self.draw_tile()
                else:
                    print("Draw mode is off")

    def draw_tile(self):
        mouse_pos = pg.mouse.get_pos()
        x = mouse_pos[0] // PygameSettings.TILE_SIZE
        y = mouse_pos[1] // PygameSettings.TILE_SIZE

        if isinstance(self.selected_tile_type, FieldType):
            self.grid[x, y] = self.selected_tile_type
        else:
            self.objects[x, y] = self.selected_tile_type

    def draw_grid(self):
        for x in range(self.sim_settings.generic.grid_size[0]):
            for y in range(self.sim_settings.generic.grid_size[1]):
                pg.draw.rect(self.screen, PygameSettings.field_colors[self.grid[x, y]],
                             pg.Rect(x * PygameSettings.TILE_SIZE, y * PygameSettings.TILE_SIZE,
                                     PygameSettings.TILE_SIZE, PygameSettings.TILE_SIZE), 0)
                if self.objects[x, y] is not ObjectType.NOTHING:
                    object = pg.transform.scale(PygameSettings.object_images[self.objects[x,y]], (PygameSettings.TILE_SIZE, PygameSettings.TILE_SIZE))
                    self.screen.blit(object, (x * PygameSettings.TILE_SIZE, y * PygameSettings.TILE_SIZE))

        for x in range(self.sim_settings.generic.grid_size[0] // 5):
            for y in range(self.sim_settings.generic.grid_size[1] // 5):
                pg.draw.rect(self.screen, (0, 0, 0, 0),
                             pg.Rect(x * PygameSettings.TILE_SIZE * 5, y * PygameSettings.TILE_SIZE * 5,
                                     PygameSettings.TILE_SIZE * 5, PygameSettings.TILE_SIZE * 5), 1)
                
        # draw the fox for test purposes
        #TODO: REMOVE
        fox = pg.image.load('assets/fox.png')
        fox = pg.transform.scale(fox, (PygameSettings.TILE_SIZE, PygameSettings.TILE_SIZE))
        self.screen.blit(fox, (100, 100))


sim = PygameSimulationTest()
sim.run()
