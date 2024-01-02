import datetime

from settings.simulation_settings import get_default_simulation_settings, SimulationSettings
from settings.pg_settings import get_default_pygame_settings, PygameSettings
from constants.enums import FieldType, ObjectType, DayPart
from framework.population_manager import PopulationManager
from framework.time_manager import TimeManager
import pygame as pg
import numpy as np
import os


class PygameSimulationTest:
    FPS: int = 5
    sim_settings: SimulationSettings
    pg_settings: PygameSettings
    grid: np.ndarray = None
    objects: np.ndarray = None
    selected_tile_type: FieldType | ObjectType
    draw_mode: bool
    debug: bool = False

    def __init__(self):
        self.sim_settings = get_default_simulation_settings()
        self.pg_settings = get_default_pygame_settings()
        self.sim_settings.generic.grid_size = (self.pg_settings.GRID_WIDTH, self.pg_settings.GRID_HEIGHT)

        self.initialize_grid()

        self.selected_tile_type = FieldType.FOREST
        self.draw_mode = False

        pg.init()
        self.screen = self.create_window()
        self.night_screen = pg.Surface((self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                                        self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[1]))
        self.night_screen.set_alpha(96)
        self.night_screen.fill((0, 0, 0))

        self.home_range_screen = pg.Surface((self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                                        self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[1]))
        self.home_range_screen.set_alpha(96)

        self.clock = pg.time.Clock()
        self.done = False

        self.time_manager = TimeManager(self.sim_settings.generic.time_step)
        self.population_manager = PopulationManager(self.sim_settings, self.grid)

        self.home_ranges = np.array([])
        self.draw_home_ranges = True

        self.food_matrix = np.array([])
        self.initialize_food_matrix()

        self.step_by_step = False  # if true, the simulation will only advance one step at a time (press enter to advance)

        self.initialize_simulation()

    def initialize_simulation(self):
        fox_dens = np.where(self.objects == ObjectType.FOX_DEN)
        self.population_manager.create_population(list(zip(*fox_dens)))
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

    def create_window(self):
        window_size = (self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                       self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[1])
        return pg.display.set_mode(window_size)

    def run(self):
        while not self.done:
            if self.draw_mode:
                self.clock.tick(60)
            else:
                self.clock.tick(self.FPS)
            self.handle_events()
            self.screen.fill((255, 255, 255))
            self.draw_grid()

            if not self.draw_mode:
                time_of_day = self.time_manager.perform_time_step()
                self.draw_time_of_day(time_of_day)
                self.draw_time()

                foxes = self.population_manager.get_foxes()
                if self.time_manager.date.hour == 0:
                    self.calculate_food_matrix(foxes)

                if self.debug:
                    print('------------------------------')
                    print(f'Population size: {len(foxes)}')
                    print(f'Food on map: {np.sum(self.food_matrix)}')
                    print(f'Max hunger: {np.max([fox.hunger for fox in foxes])}')
                    print(f'Min hunger: {np.min([fox.hunger for fox in foxes])}')
                    print(f'Average hunger: {np.mean([fox.hunger for fox in foxes])}')

                self.move_foxes(foxes, self.time_manager.date, self.objects, self.food_matrix)

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
        if pg.mouse.get_pressed()[0]:
            if self.draw_mode:
                self.draw_tile()
            else:
                print("Draw mode is off. To enable it, press space.")

    def draw_time(self):
        formatted_date = self.time_manager.date.strftime("%d/%m/%Y %H:%M:%S")
        font = pg.font.SysFont("Arial", 20)
        text = font.render(formatted_date, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def draw_tile(self):
        mouse_pos = pg.mouse.get_pos()
        x = mouse_pos[0] // self.pg_settings.TILE_SIZE
        y = mouse_pos[1] // self.pg_settings.TILE_SIZE

        x = max(min(x, self.sim_settings.generic.grid_size[0] - 1), 0)
        y = max(min(y, self.sim_settings.generic.grid_size[1] - 1), 0)

        if isinstance(self.selected_tile_type, FieldType):
            self.grid[x, y] = self.selected_tile_type
        else:
            self.objects[x, y] = self.selected_tile_type

    def draw_grid(self):
        for x in range(self.sim_settings.generic.grid_size[0]):
            for y in range(self.sim_settings.generic.grid_size[1]):
                pg.draw.rect(self.screen, self.pg_settings.field_colors[self.grid[x, y]],
                             pg.Rect(x * self.pg_settings.TILE_SIZE, y * self.pg_settings.TILE_SIZE,
                                     self.pg_settings.TILE_SIZE, self.pg_settings.TILE_SIZE), 0)
                if self.home_ranges[x, y] == 1:
                    pg.draw.rect(self.home_range_screen, (0, 255, 255),
                                 pg.Rect(x * self.pg_settings.TILE_SIZE, y * self.pg_settings.TILE_SIZE,
                                         self.pg_settings.TILE_SIZE, self.pg_settings.TILE_SIZE), 0)
                if self.objects[x, y] is not ObjectType.NOTHING:
                    obj = pg.transform.scale(self.pg_settings.object_images[self.objects[x, y]],
                                             (self.pg_settings.TILE_SIZE, self.pg_settings.TILE_SIZE))
                    self.screen.blit(obj, (x * self.pg_settings.TILE_SIZE, y * self.pg_settings.TILE_SIZE))

        if self.draw_home_ranges:
            self.screen.blit(self.home_range_screen, (0, 0))

        for x in range(self.sim_settings.generic.grid_size[0] // 5):
            for y in range(self.sim_settings.generic.grid_size[1] // 5):
                pg.draw.rect(self.screen, (0, 0, 0, 0),
                             pg.Rect(x * self.pg_settings.TILE_SIZE * 5, y * self.pg_settings.TILE_SIZE * 5,
                                     self.pg_settings.TILE_SIZE * 5, self.pg_settings.TILE_SIZE * 5), 1)

        for fox in self.population_manager.get_foxes():
            fox_pos = (int(fox.current_position.x), int(fox.current_position.y))
            fox_image = pg.transform.scale(self.pg_settings.FOX_IMAGE,
                                           (self.pg_settings.TILE_SIZE, self.pg_settings.TILE_SIZE))
            self.screen.blit(fox_image,
                             (fox_pos[0] * self.pg_settings.TILE_SIZE, fox_pos[1] * self.pg_settings.TILE_SIZE))

    def draw_time_of_day(self, time_of_day: DayPart):
        # print(self.time_manager.date, time_of_day)
        match time_of_day:
            case DayPart.NIGHT:
                self.screen.blit(self.night_screen, (0, 0))
            case DayPart.DAY:
                pass
            case DayPart.DAWN:
                self.night_screen.set_alpha(48)
                self.screen.blit(self.night_screen, (0, 0))
                self.night_screen.set_alpha(96)
            case DayPart.DUSK:
                self.night_screen.set_alpha(48)
                self.screen.blit(self.night_screen, (0, 0))
                self.night_screen.set_alpha(96)

    def move_foxes(self, foxes, date, objects, food_matrix):
        for fox in foxes:
            fox.move(date, objects, food_matrix)

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
                self.food_matrix[x, y] += max(0, np.random.normal(0, 0.25) / max(1, fox_count))  # adjustable


sim = PygameSimulationTest()
sim.run()
