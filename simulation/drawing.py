import numpy as np

from simulation.simulation import PygameSimulation
from constants.enums import FieldType
import pygame as pg


class AntRenderer(PygameSimulation.IRenderer):
    def draw_text(self, sim: PygameSimulation):
        font = pg.font.SysFont("Arial", 20)
        text = font.render("paused" if sim.paused else "running", True, (255, 0, 0))
        sim.screen.blit(text, (10, 10))

    def tile_at_mouse_pos(self, sim: PygameSimulation):
        mouse_pos = pg.mouse.get_pos()
        x = mouse_pos[0] // sim.sim_settings.generic.tile_size
        y = mouse_pos[1] // sim.sim_settings.generic.tile_size

        x = max(min(x, sim.sim_settings.generic.grid_size[0] - 1), 0)
        y = max(min(y, sim.sim_settings.generic.grid_size[1] - 1), 0)

        if isinstance(sim.selected_tile_type, FieldType):
            sim.grid[x, y] = sim.selected_tile_type
        else:
            # Initialize sim.objects if it's None
            if sim.objects is None:
                sim.objects = np.full(sim.sim_settings.generic.grid_size, None)

            if sim.nodes[x][y] is not None:
                sim.objects[x, y] = sim.selected_tile_type
            else:
                print("select field on path to place object")

        return x, y

    def draw_grid(self, sim: PygameSimulation):
        for x in range(sim.grid.shape[0]):
            for y in range(sim.grid.shape[1]):
                pg.draw.rect(sim.screen, sim.display_settings.field_colors[sim.grid[x, y]],
                             pg.Rect(x * sim.sim_settings.generic.tile_size, y * sim.sim_settings.generic.tile_size,
                                     sim.sim_settings.generic.tile_size, sim.sim_settings.generic.tile_size), 0)

    def draw_population(self, sim: PygameSimulation):
        population = sim.population
        for ant in population.ants:
            ax, ay = ant.pos
            tile = sim.sim_settings.generic.tile_size
            rect_size = tile // 4
            offset = rect_size
            r = pg.rect.Rect(ax * tile + offset, ay * tile + offset, rect_size, rect_size)
            pg.draw.rect(sim.screen, ant.color, r)
            scaled = pg.transform.scale(sim.display_settings.ant_image,
                                        (sim.sim_settings.generic.tile_size,
                                         sim.sim_settings.generic.tile_size))
            sim.screen.blit(scaled, (ax * sim.sim_settings.generic.tile_size, ay * sim.sim_settings.generic.tile_size))

    def draw_pheromones(self, sim: PygameSimulation):
        TMP_PHEROMONE_FLAVOR = sim.sim_settings.generic.source  # Assuming this flavor is valid
        # Define the size of the pheromone surface
        pheromone_surface = pg.Surface(
            (sim.sim_settings.generic.grid_size[0] * sim.sim_settings.generic.tile_size,
             sim.sim_settings.generic.grid_size[1] * sim.sim_settings.generic.tile_size),
            flags=pg.SRCALPHA
        )

        # Loop over the entire grid and draw pheromones
        for x in range(sim.sim_settings.generic.grid_size[0]):
            for y in range(sim.sim_settings.generic.grid_size[1]):
                node = sim.nodes[x][y]
                if node is not None:  # Only process nodes for valid areas
                    intensity = node.get_pheromone_intensity()
                    # Adjust color intensity based on the intensity value
                    color = (255, 0, 0, int(150 * intensity))  # RGBA, adjust transparency based on intensity
                    tile_size = sim.sim_settings.generic.tile_size

                    # Render pheromone intensity as a tile with varying alpha transparency
                    pg.draw.rect(
                        pheromone_surface,
                        color,
                        pg.Rect(x * tile_size, y * tile_size, tile_size, tile_size),
                        0  # Fill the tile completely
                    )

        # Blit the pheromone surface onto the main screen
        sim.screen.blit(pheromone_surface, (0, 0))

    def draw_source_and_target(self, sim: PygameSimulation):
        if sim.source is not None:
            sx, sy = sim.source
            scaled = pg.transform.scale(sim.display_settings.colony_image,
                                        (sim.sim_settings.generic.tile_size,
                                         sim.sim_settings.generic.tile_size))
            sim.screen.blit(scaled, (sx * sim.sim_settings.generic.tile_size, sy * sim.sim_settings.generic.tile_size))
        if sim.target is not None:
            tx, ty = sim.target
            scaled = pg.transform.scale(sim.display_settings.food_image,
                                        (sim.sim_settings.generic.tile_size,
                                         sim.sim_settings.generic.tile_size))
            sim.screen.blit(scaled, (tx * sim.sim_settings.generic.tile_size, ty * sim.sim_settings.generic.tile_size))

    def draw(self, sim: PygameSimulation):
        self.draw_grid(sim)
        if sim.show_pheromones:
            self.draw_pheromones(sim)
        if sim.show_ants:
            self.draw_population(sim)
        self.draw_source_and_target(sim)
        self.draw_text(sim)
