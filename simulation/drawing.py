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
        x = mouse_pos[0] // sim.display_settings.TILE_SIZE
        y = mouse_pos[1] // sim.display_settings.TILE_SIZE

        x = max(min(x, sim.sim_settings.generic.grid_size[0] - 1), 0)
        y = max(min(y, sim.sim_settings.generic.grid_size[1] - 1), 0)

        if isinstance(sim.selected_tile_type, FieldType):
            sim.grid[x, y] = sim.selected_tile_type
        else:
            sim.objects[x, y] = sim.selected_tile_type

    def draw_grid(self, sim: PygameSimulation):
        print(sim.grid.shape)
        for x in range(sim.sim_settings.generic.grid_size[0]):
            for y in range(sim.sim_settings.generic.grid_size[1]):
                pg.draw.rect(sim.screen, sim.display_settings.field_colors[sim.grid[x, y]],
                                pg.Rect(x * sim.display_settings.TILE_SIZE, y * sim.display_settings.TILE_SIZE,
                                        sim.display_settings.TILE_SIZE, sim.display_settings.TILE_SIZE), 0)

    def draw_colonies(self, sim: PygameSimulation):
        for colony in sim.colonies:
            cx, cy = colony.pos
            scaled = pg.transform.scale(sim.display_settings.colony_image,
                (sim.display_settings.TILE_SIZE,
                    sim.display_settings.TILE_SIZE))
            sim.screen.blit(scaled, (cx * sim.display_settings.TILE_SIZE, cy * sim.display_settings.TILE_SIZE))
            for ant in colony.ants:
                ax, ay = ant.pos
                scaled = pg.transform.scale(sim.display_settings.ant_image,
                    (sim.display_settings.TILE_SIZE,
                    sim.display_settings.TILE_SIZE))
                sim.screen.blit(scaled, (ax * sim.display_settings.TILE_SIZE, ay * sim.display_settings.TILE_SIZE))
            for food in colony.foods:
                fx, fy = food
                scaled = pg.transform.scale(sim.display_settings.food_image,
                (sim.display_settings.TILE_SIZE,
                 sim.display_settings.TILE_SIZE))
                sim.screen.blit(scaled, (fx * sim.display_settings.TILE_SIZE, fy * sim.display_settings.TILE_SIZE))

    def draw_pheromones(self, sim: PygameSimulation):
        TMP_PHEROMONE_FLAVOR = 0 # TODO switch between flavors
        for x in range(sim.sim_settings.generic.grid_size[0]):
            for y in range(sim.sim_settings.generic.grid_size[1]):
                color = (int(255 * sim.nodes[x][y].mean_intensity(TMP_PHEROMONE_FLAVOR)), 0, 0)
                pg.draw.rect(
                    sim.screen,
                    color,
                    pg.Rect(
                        x * sim.display_settings.TILE_SIZE,
                        y * sim.display_settings.TILE_SIZE,
                        sim.display_settings.TILE_SIZE,
                        sim.display_settings.TILE_SIZE
                    ),
                0)


    def draw(self, sim: PygameSimulation):
        self.draw_grid(sim)
        if sim.show_pheromones:
            self.draw_pheromones(sim)
        self.draw_colonies(sim)
        self.draw_text(sim)