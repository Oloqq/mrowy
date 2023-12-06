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


@dataclass
class PygameSettings:
    TILE_SIZE = 20
    field_colors = {
        FieldType.GRASS: (0, 255, 0),
        FieldType.FOREST: (0, 100, 0),
        FieldType.WATER: (0, 0, 255),
        FieldType.URBAN: (100, 100, 100)
    }


class PygameSimulationTest:
    FPS = 30

    def __init__(self):
        self.sim_settings = get_default_settings()
        self.sim_settings.generic.grid_size = (30, 50)
        self.pg_settings = PygameSettings()

        if os.path.exists("grid.npy"):
            loaded_grid = np.load("grid.npy", allow_pickle=True)
            if loaded_grid.shape == self.sim_settings.generic.grid_size:
                print("Loaded grid from file")
                self.grid = loaded_grid
        else:
            print("Created new grid")
            self.grid = np.full(self.sim_settings.generic.grid_size, FieldType.GRASS, dtype=FieldType)

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
                elif event.key == pg.K_s:
                    np.save("grid.npy", self.grid)
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
        self.grid[x, y] = self.selected_tile_type

    def draw_grid(self):
        for x in range(self.sim_settings.generic.grid_size[0]):
            for y in range(self.sim_settings.generic.grid_size[1]):
                pg.draw.rect(self.screen, PygameSettings.field_colors[self.grid[x, y]],
                             pg.Rect(x * PygameSettings.TILE_SIZE, y * PygameSettings.TILE_SIZE,
                                     PygameSettings.TILE_SIZE, PygameSettings.TILE_SIZE), 0)

        for x in range(self.sim_settings.generic.grid_size[0] // 5):
            for y in range(self.sim_settings.generic.grid_size[1] // 5):
                pg.draw.rect(self.screen, (0, 0, 0, 0),
                             pg.Rect(x * PygameSettings.TILE_SIZE * 5, y * PygameSettings.TILE_SIZE * 5,
                                     PygameSettings.TILE_SIZE * 5, PygameSettings.TILE_SIZE * 5), 1)


sim = PygameSimulationTest()
sim.run()
