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

    def __init__(self):
        self.sim_settings = get_default_simulation_settings()
        self.pg_settings = get_default_pygame_settings()
        self.sim_settings.generic.grid_size = (self.pg_settings.GRID_WIDTH, self.pg_settings.GRID_HEIGHT)

        self.initialize_grid()

        self.selected_tile_type = FieldType.FOREST
        self.draw_mode = True

        pg.init()
        self.screen = self.create_window()
        self.night_screen = pg.Surface((self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[0],
                                        self.pg_settings.TILE_SIZE * self.sim_settings.generic.grid_size[1]))
        self.night_screen.set_alpha(128)
        self.night_screen.fill((0, 0, 0))
        self.clock = pg.time.Clock()
        self.done = False

        self.time_manager = TimeManager(self.sim_settings.generic.time_step)
        self.population_manager = PopulationManager(self.sim_settings)

        self.home_ranges = np.array([])
        self.draw_home_ranges = True

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
            self.clock.tick(self.FPS)
            self.handle_events()
            self.screen.fill((255, 255, 255))
            self.draw_grid()

            time_of_day = self.time_manager.perform_time_step()
            self.draw_time_of_day(time_of_day)

            # movement of foxes - it is the only change here
            foxes = self.population_manager.get_foxes()
            self.move_foxes(foxes, self.time_manager.date.hour, self.objects)

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
                    np.savez(self.pg_settings.SAVE_NAME, grid=self.grid, objects=self.objects)
                    print("Saved grid to file")
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.draw_mode:
                    self.draw_tile()
                else:
                    print("Draw mode is off")

    def draw_tile(self):
        mouse_pos = pg.mouse.get_pos()
        x = mouse_pos[0] // self.pg_settings.TILE_SIZE
        y = mouse_pos[1] // self.pg_settings.TILE_SIZE

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
                if self.home_ranges[x, y] == 1 and self.draw_home_ranges:
                    pg.draw.rect(self.screen, (0, 255, 255),
                                 pg.Rect(x * self.pg_settings.TILE_SIZE, y * self.pg_settings.TILE_SIZE,
                                         self.pg_settings.TILE_SIZE, self.pg_settings.TILE_SIZE), 0)
                if self.objects[x, y] is not ObjectType.NOTHING:
                    obj = pg.transform.scale(self.pg_settings.object_images[self.objects[x, y]],
                                             (self.pg_settings.TILE_SIZE, self.pg_settings.TILE_SIZE))
                    self.screen.blit(obj, (x * self.pg_settings.TILE_SIZE, y * self.pg_settings.TILE_SIZE))

        for x in range(self.sim_settings.generic.grid_size[0] // 5):
            for y in range(self.sim_settings.generic.grid_size[1] // 5):
                pg.draw.rect(self.screen, (0, 0, 0, 0),
                             pg.Rect(x * self.pg_settings.TILE_SIZE * 5, y * self.pg_settings.TILE_SIZE * 5,
                                     self.pg_settings.TILE_SIZE * 5, self.pg_settings.TILE_SIZE * 5), 1)

        # display foxes
        for fox in self.population_manager.get_foxes():
            fox_pos = (int(fox.current_position.x), int(fox.current_position.y))
            fox_image = pg.transform.scale(self.pg_settings.FOX_IMAGE,
                                           (self.pg_settings.TILE_SIZE, self.pg_settings.TILE_SIZE))
            self.screen.blit(fox_image,
                             (fox_pos[0] * self.pg_settings.TILE_SIZE, fox_pos[1] * self.pg_settings.TILE_SIZE))

    def draw_time_of_day(self, time_of_day: DayPart):
        #print(self.time_manager.date, time_of_day)
        if time_of_day == DayPart.NIGHT:
            self.screen.blit(self.night_screen, (0, 0))

    def move_foxes(self, foxes, hour, objects):
        for fox in foxes:
            fox.move(hour, objects)


sim = PygameSimulationTest()
sim.run()
