from simulation.simulation import PygameSimulation
from constants.enums import FieldType, ObjectType, DayPart, Sex

import pygame as pg

class FoxRenderer(PygameSimulation.IRenderer):
    def draw_time(self, sim: PygameSimulation):
        formatted_date = sim.time_manager.date.strftime("%d/%m/%Y %H:%M:%S")
        font = pg.font.SysFont("Arial", 20)
        text = font.render(formatted_date, True, (255, 255, 255))
        sim.screen.blit(text, (10, 10))

    def draw_tile(self, sim: PygameSimulation):
        mouse_pos = pg.mouse.get_pos()
        x = mouse_pos[0] // sim.pg_settings.TILE_SIZE
        y = mouse_pos[1] // sim.pg_settings.TILE_SIZE

        x = max(min(x, sim.sim_settings.generic.grid_size[0] - 1), 0)
        y = max(min(y, sim.sim_settings.generic.grid_size[1] - 1), 0)

        if isinstance(sim.selected_tile_type, FieldType):
            sim.grid[x, y] = sim.selected_tile_type
        else:
            sim.objects[x, y] = sim.selected_tile_type

    def draw_grid(self, sim: PygameSimulation):
        for x in range(sim.sim_settings.generic.grid_size[0]):
            for y in range(sim.sim_settings.generic.grid_size[1]):
                pg.draw.rect(sim.screen, sim.pg_settings.field_colors[sim.grid[x, y]],
                                pg.Rect(x * sim.pg_settings.TILE_SIZE, y * sim.pg_settings.TILE_SIZE,
                                        sim.pg_settings.TILE_SIZE, sim.pg_settings.TILE_SIZE), 0)
                if sim.home_ranges[x, y] == 1:
                    pg.draw.rect(sim.home_range_screen, (0, 255, 255),
                                    pg.Rect(x * sim.pg_settings.TILE_SIZE, y * sim.pg_settings.TILE_SIZE,
                                            sim.pg_settings.TILE_SIZE, sim.pg_settings.TILE_SIZE), 0)
                if sim.objects[x, y] is not ObjectType.NOTHING:
                    obj = pg.transform.scale(sim.pg_settings.object_images[sim.objects[x, y]],
                                                (sim.pg_settings.TILE_SIZE, sim.pg_settings.TILE_SIZE))
                    sim.screen.blit(obj, (x * sim.pg_settings.TILE_SIZE, y * sim.pg_settings.TILE_SIZE))

        if sim.draw_home_ranges:
            sim.screen.blit(sim.home_range_screen, (0, 0))

        for x in range(sim.sim_settings.generic.grid_size[0] // 5):
            for y in range(sim.sim_settings.generic.grid_size[1] // 5):
                pg.draw.rect(sim.screen, (0, 0, 0, 0),
                                pg.Rect(x * sim.pg_settings.TILE_SIZE * 5, y * sim.pg_settings.TILE_SIZE * 5,
                                        sim.pg_settings.TILE_SIZE * 5, sim.pg_settings.TILE_SIZE * 5), 1)

        for fox in sim.population_manager.get_foxes():
            fox_pos = (int(fox.current_position.x), int(fox.current_position.y))
            fox_image = pg.transform.scale(sim.pg_settings.FOX_IMAGE,
                                            (sim.pg_settings.TILE_SIZE, sim.pg_settings.TILE_SIZE))
            sim.screen.blit(fox_image,
                                (fox_pos[0] * sim.pg_settings.TILE_SIZE, fox_pos[1] * sim.pg_settings.TILE_SIZE))

        hunter_image = pg.transform.scale(sim.pg_settings.object_images[ObjectType.HUNTER],
                                            (sim.pg_settings.TILE_SIZE, sim.pg_settings.TILE_SIZE))
        sim.screen.blit(hunter_image,
                            (sim.hunter.position[0] * sim.pg_settings.TILE_SIZE, sim.hunter.position[1] * sim.pg_settings.TILE_SIZE))

    def draw_time_of_day(self, sim: PygameSimulation, time_of_day: DayPart):
        # print(sim.time_manager.date, time_of_day)
        match time_of_day:
            case DayPart.NIGHT:
                sim.screen.blit(sim.night_screen, (0, 0))
            case DayPart.DAY:
                pass
            case DayPart.DAWN:
                sim.night_screen.set_alpha(48)
                sim.screen.blit(sim.night_screen, (0, 0))
                sim.night_screen.set_alpha(96)
            case DayPart.DUSK:
                sim.night_screen.set_alpha(48)
                sim.screen.blit(sim.night_screen, (0, 0))
                sim.night_screen.set_alpha(96)


    def draw(self, sim: PygameSimulation):
        self.draw_grid(sim)
        time_of_day = sim.time_manager.perform_time_step()
        self.draw_time_of_day(sim, time_of_day)
        self.draw_time(sim)