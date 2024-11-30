from collections import OrderedDict
from simulation.ant import Ant
from simulation.node import Node
from settings.simulation_settings import SimulationSettings
from PIL import Image, ImageDraw
from pygame import Vector2
import numpy as np


def output_shortest_path_on_source_img(shortest_path: OrderedDict, source_img_path: str,
                                       output_img_path: str, tile_size: int):
    """
    Overlays the shortest path on the source image and saves it to a file.
    """
    try:
        # Open the source image
        source_img = Image.open(source_img_path).convert("RGB")  # Ensure the image is in RGB mode
        draw = ImageDraw.Draw(source_img)

        # Convert grid coordinates to pixel coordinates
        pixel_path = [(x, y)
                      for x, y in shortest_path.keys()]

        # Debugging: Ensure pixel path is correct
        print("Pixel Path:", pixel_path)

        # Draw the path if it contains more than one point
        if len(pixel_path) > 1:
            draw.line(pixel_path, fill=(255, 0, 0), width=1)  # Draw the path in red
        else:
            print("Shortest path is too short to be drawn.")

        # Save the output image
        source_img.save(output_img_path)
        print(f"Shortest path overlay saved to {output_img_path}")

    except Exception as e:
        print(f"Error while processing the shortest path visualization: {e}")


class Population:
    def __init__(self, sim_settings: SimulationSettings):
        self.sim_settings = sim_settings
        self.spawn_interval = sim_settings.population.spawn_interval
        self.time_to_spawn = sim_settings.population.spawn_interval
        self.ants: list[Ant] = []
        self.foods = [Vector2(7, 7)]  # For visualization, can be removed later
        self.ant_life_iteration = 0

    def step(self, grid: np.ndarray, objects: np.ndarray, nodes: list[list[Node]]):
        """
        Executes one simulation step, updating ants and generating the shortest path visualization if applicable.
        """

        assert len(self.foods) == 1

        # Handle spawning and selection of ants
        self.time_to_spawn -= 1
        if self.time_to_spawn <= 0 or len(self.ants) == 0:
            self.ant_life_iteration += 1

            minimum_shortest_path_to_destination = self.sim_settings.population.ant_max_memory
            shortest_path = OrderedDict()
            new_ants = []

            if self.ants:
                # Find the shortest path among returning ants
                for ant in self.ants:
                    if ant.is_returning and len(ant.visited_fields_copy) < minimum_shortest_path_to_destination:
                        minimum_shortest_path_to_destination = len(ant.visited_fields_copy)
                        shortest_path = ant.visited_fields_copy

                # Filter ants with paths near the shortest path length
                new_ants = [
                    ant for ant in self.ants
                    if ant.is_returning and len(ant.visited_fields_copy) < 1.2 * minimum_shortest_path_to_destination
                ]

                # If a sufficiently short path is found, visualize it
                if minimum_shortest_path_to_destination < self.sim_settings.population.ant_max_memory:
                    filename = f"results/output_with_path_{self.ant_life_iteration}.png"
                    output_shortest_path_on_source_img(
                        shortest_path,
                        self.sim_settings.generic.map_image_path,
                        filename,
                        self.sim_settings.generic.tile_size
                    )

            # Update ant population
            self.ants = new_ants
            print(f"{len(self.ants)} ants had paths shorter than 1.2x the shortest. "
                  f"Minimum path length: {minimum_shortest_path_to_destination}")

            self.time_to_spawn = self.spawn_interval
            additional_ants = self.sim_settings.population.population_size - len(self.ants)
            print(f"Next generation: adding {additional_ants} new ants.")

            for _ in range(additional_ants):
                self.ants.append(
                    Ant(
                        position=self.sim_settings.generic.source,
                        destination=self.sim_settings.generic.target,
                        destination_bonus=self.sim_settings.population.destination_bonus,
                        max_memory=self.sim_settings.population.ant_max_memory
                    )
                )

        # Perform a step for each ant and remove any that are ready to die
        for ant in self.ants:
            ant.step(grid, objects, nodes)

        self.ants = [ant for ant in self.ants if not ant.ready_to_die]
