from settings.simulation_settings import SimulationSettings
from settings.display_settings import DisplaySettings
from constants.enums import FieldType, ObjectType, DayPart, Sex

from simulation import initialize
from simulation.population import Population

import pygame as pg
import numpy as np

MAX_FPS = 60

class PygameSimulation:
    class IRenderer:
        def draw(sim: "PygameSimulation"):
            raise NotImplementedError

        def draw_tile(sim: "PygameSimulation"):
            raise NotImplementedError

    def __init__(self, save_name: str, renderer: IRenderer, sim_settings: SimulationSettings, display_settings: DisplaySettings):
        self.save_name = save_name
        self.sim_settings: SimulationSettings = sim_settings
        self.display_settings: DisplaySettings = display_settings
        old_grid_size = (self.display_settings.GRID_WIDTH_OLD, self.display_settings.GRID_HEIGHT_OLD)
        new_grid_size = (self.display_settings.GRID_WIDTH_NEW, self.display_settings.GRID_HEIGHT_NEW)
        self.sim_settings.generic.grid_size = new_grid_size if sim_settings.generic.create_grid_from_img else old_grid_size
        self.sim_settings.generic.tile_size = self.display_settings.TILE_SIZE_NEW if sim_settings.generic.create_grid_from_img else self.display_settings.TILE_SIZE_OLD

        # display
        pg.init()
        self.renderer = renderer
        self.screen = initialize.window(sim_settings)
        self.grid, self.objects, self.nodes = initialize.grid_and_objects(save_name, sim_settings)
        self.show_pheromones = True
        self.show_ants = True

        # app state
        self.selected_tile_type: FieldType | ObjectType = FieldType.GRASS
        self.done = False
        self.paused = True
        self.debug = False
        self.step_by_step = True
        self.step_requested = False


        # simulation logic
        # self.trips = [ # use for displaying paths
        #     ((0, 2), (0, 10))
        # ]
        self.population: Population = Population()

    def run(self):
        clock = pg.time.Clock()
        while not self.done:
            clock.tick(MAX_FPS)
            self.handle_events()

            need_to_step = self.step_by_step and self.step_requested
            if not self.paused or need_to_step:
                self.step_requested = False
                self.population.step(self.grid, self.objects, self.nodes)

            self.screen.fill((255, 255, 255))
            self.renderer.draw(self)

            pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                elif event.key == pg.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pg.K_TAB:
                    if self.step_by_step:
                        self.step_requested = True
                elif event.key == pg.K_1:
                    self.selected_tile_type = FieldType.GRASS
                    print("Selected grass")
                elif event.key == pg.K_2:
                    self.selected_tile_type = FieldType.FOREST
                    print("Selected forest")
                elif event.key == pg.K_3:
                    self.selected_tile_type = FieldType.WATER
                    print("Selected water")
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
                    np.savez(self.save_name, grid=self.grid, objects=self.objects)
                    print("Saved grid to file")
                elif event.key == pg.K_p:
                    self.step_by_step = not self.step_by_step
                elif event.key == pg.K_f:
                    self.show_pheromones = not self.show_pheromones
                elif event.key == pg.K_a:
                    self.show_ants = not self.show_ants
        if pg.mouse.get_pressed()[0]:
            if self.paused:
                # TODO nodes have to be updated as well
                self.renderer.draw_tile(self)
            else:
                print("Draw mode is off. To enable it, press space.")
