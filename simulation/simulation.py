from settings.simulation_settings import get_default_simulation_settings, SimulationSettings
from settings.pg_settings import get_default_pygame_settings, PygameSettings
from constants.enums import FieldType, ObjectType, DayPart, Sex
from framework.population_manager import PopulationManager
from framework.time_manager import TimeManager
from framework.plot import plot
from agents.hunter import Hunter
from agents.fox import Fox

import pygame as pg
import numpy as np
import os

MAX_FPS = 10

class PygameSimulation:
    class IRenderer:
        def draw(sim: "PygameSimulation"):
            raise NotImplementedError

        def draw_tile(sim: "PygameSimulation"):
            raise NotImplementedError

    def __init__(self, renderer: IRenderer):
        self.renderer = renderer

        self.grid: np.ndarray = None
        self.objects: np.ndarray = None
        self.fox_stats: np.ndarray = None
        self.mean_scores: np.ndarray = None

        self.sim_settings: SimulationSettings = get_default_simulation_settings()
        self.pg_settings: PygameSettings = get_default_pygame_settings()
        self.sim_settings.generic.grid_size = (self.pg_settings.GRID_WIDTH, self.pg_settings.GRID_HEIGHT)

        self.rabbits_in_dens = {}
        self.initialize_grid()

        self.selected_tile_type: FieldType | ObjectType = FieldType.FOREST
        self.paused = False
        self.debug = True

        pg.init()
        self.screen = self.create_window()
        self.night_screen = pg.Surface((self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                                        self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[1]))
        self.night_screen.set_alpha(96)
        self.night_screen.fill((0, 0, 0))

        self.home_range_screen = pg.Surface((self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                                        self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[1]))
        self.home_range_screen.set_alpha(96)

        self.done = False

        self.time_manager = TimeManager(self.sim_settings.generic.time_step)
        self.population_manager = PopulationManager(self.sim_settings, self.grid)

        self.home_ranges = np.array([])
        self.draw_home_ranges = True

        self.food_matrix = np.array([])
        self.initialize_food_matrix()

        self.hunter = Hunter(self.sim_settings.fox.shooting, self.population_manager, self.objects)

        self.step_by_step = False  # if true, the simulation will only advance one step at a time (press enter to advance)

        self.fox_stats = np.empty(shape=[0])
        self.mean_scores = np.empty(shape=[0])

        self.initialize_simulation()

    def initialize_simulation(self):
        fox_dens = np.where(self.objects == ObjectType.FOX_DEN)
        self.population_manager.create_population(list(zip(*fox_dens)), self.time_manager.date)
        self.home_ranges = np.full(self.sim_settings.generic.grid_size, 0, dtype=object)

        for fox in self.population_manager.get_foxes():
            for pos in fox.home_range:
                if 0 <= pos[0] < self.sim_settings.generic.grid_size[0] and \
                        0 <= pos[1] < self.sim_settings.generic.grid_size[1]:
                    self.home_ranges[pos] = 1

    def initialize_grid(self):
        if os.path.exists(self.pg_settings.SAVE_NAME):
            loaded_data = np.load(self.pg_settings.SAVE_NAME, allow_pickle=True)
            loaded_grid = loaded_data['grid']
            loaded_objects = loaded_data['objects']
            if (loaded_grid.shape == self.sim_settings.generic.grid_size and
                    loaded_objects.shape == self.sim_settings.generic.grid_size):
                print("Loaded grid from file")
                self.grid = loaded_grid
                self.objects = loaded_objects
            elif loaded_grid.shape != self.sim_settings.generic.grid_size:
                raise ValueError(f"Grid size in file does not match simulation settings\n"
                                 f"Grid size in file: {loaded_grid.shape}\n"
                                 f"Expected grid size: {self.sim_settings.generic.grid_size}")
            else:
                raise ValueError(f"Object grid size in file does not match simulation settings\n"
                                 f"Grid size in file: {loaded_objects.shape}\n"
                                 f"Expected grid size: {self.sim_settings.generic.grid_size}")
        else:
            print("Created new grid")
            self.grid = np.full(self.sim_settings.generic.grid_size, FieldType.GRASS, dtype=FieldType)
            self.objects = np.full(self.sim_settings.generic.grid_size, ObjectType.NOTHING, dtype=ObjectType)

        yy, xx = self.objects.shape
        for y in range(yy):
            for x in range(xx):
                if self.objects[y, x] == ObjectType.RABBIT_DEN:
                    self.rabbits_in_dens[(y, x)] = 15


    def create_window(self):
        window_size = (self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                       self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[1])
        return pg.display.set_mode(window_size)

    def run(self):
        clock = pg.time.Clock()
        while not self.done:
            self.handle_events()

            if self.paused:
                continue

            clock.tick(MAX_FPS)
            self.screen.fill((255, 255, 255))
            self.renderer.draw(self)

            foxes = self.population_manager.get_foxes()
            if self.time_manager.date.hour == 0:
                self.calculate_food_matrix(foxes)
            if self.time_manager.date.hour == 23:
                self.hunter.hunt(self.time_manager.date, foxes)

            if self.debug:
                male_foxes = 0
                for fox in foxes:
                    if fox.sex == Sex.MALE:
                        male_foxes += 1
                print('------------------------------')
                print(f'Population size: {len(foxes)}, Male foxes: {male_foxes}, Female foxes: {len(foxes)-male_foxes}')
                print(f'Food on map: {np.sum(self.food_matrix)}')
                print(f'Max hunger: {np.max([fox.hunger for fox in foxes])}')
                print(f'Min hunger: {np.min([fox.hunger for fox in foxes])}')
                print(f'Average hunger: {np.mean([fox.hunger for fox in foxes])}')


            if self.time_manager.date.hour == 1:
                for rabbit in self.rabbits_in_dens.keys():
                    self.rabbits_in_dens[rabbit] = 15

                if self.time_manager.date.weekday() == 1:
                    self.fox_stats = np.append(self.fox_stats, [len(foxes)])
                    self.mean_scores = np.append(self.mean_scores, [round(np.mean(self.fox_stats), 2)])
                if self.time_manager.date.day == 1 and len(self.fox_stats) > 0:
                    plot(self.fox_stats, self.mean_scores)

            if self.time_manager.date.year == 2030:
                self.done = True

            self.move_foxes(foxes, self.time_manager.date, self.objects, self.food_matrix, self.rabbits_in_dens)
            # print(self.time_manager.date.hour, self.rabbits_in_dens)

            if self.step_by_step:
                self.wait_for_space()

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
                    np.savez(self.pg_settings.SAVE_NAME, grid=self.grid, objects=self.objects)
                    print("Saved grid to file")
                elif event.key == pg.K_p:
                    self.step_by_step = not self.step_by_step
        # REVIEW jaki to ma cel
        if pg.mouse.get_pressed()[0]:
            if self.paused:
                self.renderer.draw_tile(self)
            else:
                print("Draw mode is off. To enable it, press space.")

    def move_foxes(self, foxes, date, objects, food_matrix, rabbits_in_dens):
        for fox in reversed(foxes):
            fox.move(date, objects, food_matrix, rabbits_in_dens)

    def wait_for_space(self):
        stop_flag = 1
        while stop_flag > 0 and not self.done:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        stop_flag = 0
                    elif event.key == pg.K_p:
                        self.step_by_step = not self.step_by_step
                        stop_flag = 0
                    elif event.key == pg.K_ESCAPE:
                        self.done = True
                elif event.type == pg.QUIT:
                    self.done = True

    def initialize_food_matrix(self):
        self.food_matrix = np.zeros((self.sim_settings.generic.grid_size[0],
                                    self.sim_settings.generic.grid_size[1]))
        self.calculate_food_matrix(self.population_manager.get_foxes())

    def calculate_food_matrix(self, foxes):
        for x in range(self.sim_settings.generic.grid_size[0]):
            for y in range(self.sim_settings.generic.grid_size[1]):
                neighborhood_x = slice(max(0, x - 1), min(self.sim_settings.generic.grid_size[0], x + 2))
                neighborhood_y = slice(max(0, y - 1), min(self.sim_settings.generic.grid_size[1], y + 2))

                fox_count = sum(
                    1 for fox in foxes if
                    neighborhood_x.start <= fox.current_position.x < neighborhood_x.stop and
                    neighborhood_y.start <= fox.current_position.y < neighborhood_y.stop
                )
                self.food_matrix[x, y] += max(0, np.random.normal(0, 0.05))  # adjustable
