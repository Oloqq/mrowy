from simulation.simulation import PygameSimulation
from simulation.node import Node
from constants.enums import FieldType, ObjectType, DayPart, Sex
import pygame as pg

class AntRenderer(PygameSimulation.IRenderer):
    def draw_text(self, sim: PygameSimulation):
        font = pg.font.SysFont("Arial", 20)
        text = font.render("paused" if sim.paused else "running", True, (255, 0, 0))
        sim.screen.blit(text, (10, 10))

    def draw_tile(self, sim: PygameSimulation):
        mouse_pos = pg.mouse.get_pos()
        x = mouse_pos[0] // sim.sim_settings.generic.tile_size
        y = mouse_pos[1] // sim.sim_settings.generic.tile_size

        x = max(min(x, sim.sim_settings.generic.grid_size[0] - 1), 0)
        y = max(min(y, sim.sim_settings.generic.grid_size[1] - 1), 0)

        if isinstance(sim.selected_tile_type, FieldType):
            sim.grid[x, y] = sim.selected_tile_type
        else:
            sim.objects[x, y] = sim.selected_tile_type

    def draw_grid(self, sim: PygameSimulation):
        for x in range(sim.grid.shape[0]):
            for y in range(sim.grid.shape[1]):
                pg.draw.rect(sim.screen, sim.display_settings.field_colors[sim.grid[x, y]],
                                pg.Rect(x * sim.sim_settings.generic.tile_size, y * sim.sim_settings.generic.tile_size,
                                        sim.sim_settings.generic.tile_size, sim.sim_settings.generic.tile_size), 0)

    def draw_population(self, sim: PygameSimulation):
        population = sim.population
        for ant in population.ants:
            if ant.source != (7, 7) and ant.destination != (7, 7):
                continue

            ax, ay = ant.pos
            tile = sim.sim_settings.generic.tile_size
            rect_size = tile // 4
            offset = rect_size
            r = pg.rect.Rect(ax * tile + offset, ay * tile + offset, rect_size, rect_size)
            pg.draw.rect(sim.screen, ant.color, r)
            # scaled = pg.transform.scale(sim.display_settings.ant_image,
            #     (sim.sim_settings.generic.tile_size,
            #     sim.sim_settings.generic.tile_size))
            # sim.screen.blit(scaled, (ax * sim.sim_settings.generic.tile_size, ay * sim.sim_settings.generic.tile_size))
        for food in population.foods:
            fx, fy = food
            scaled = pg.transform.scale(sim.display_settings.food_image,
            (sim.sim_settings.generic.tile_size,
                sim.sim_settings.generic.tile_size))
            sim.screen.blit(scaled, (fx * sim.sim_settings.generic.tile_size, fy * sim.sim_settings.generic.tile_size))

    def draw_pheromones(self, sim: PygameSimulation):
        TMP_PHEROMONE_FLAVOR = (7, 7) # TODO switch between flavors
        for x in range(sim.sim_settings.generic.grid_size[0]):
            for y in range(sim.sim_settings.generic.grid_size[1]):
                color = (int(255 * sim.nodes[x][y].mean_intensity(TMP_PHEROMONE_FLAVOR, x, y, sim.nodes)), 0, 0)
                pg.draw.rect(
                    sim.screen,
                    color,
                    pg.Rect(
                        x * sim.sim_settings.generic.tile_size,
                        y * sim.sim_settings.generic.tile_size,
                        sim.sim_settings.generic.tile_size,
                        sim.sim_settings.generic.tile_size
                    ),
                0)


    def draw(self, sim: PygameSimulation):
        self.draw_grid(sim)
        if sim.show_pheromones:
            self.draw_pheromones(sim)
        if sim.show_ants:
            self.draw_population(sim)
        self.draw_text(sim)