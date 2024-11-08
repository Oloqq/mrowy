from constants.enums import DistributionType, TimeStep, Sex
from dataclasses import dataclass, field
from simulation.ant import Coords

@dataclass
class GenericSimulationSettings:
    """
    Simulation metadata and other implementation details.

    Attributes:
        grid_size: The size of the grid in (x, y) format.
        tile_size: The size of a single tile in the grid in meters.
        time_step: The time step of the simulation.
        duration: The duration of the simulation in time steps.
        map_image_path: The path to the image file used to generate the grid.
    """
    grid_size: tuple[int, int] = (100, 100)
    time_step: TimeStep = TimeStep.HOURLY
    tile_size: int = 5
    duration: int = 1000
    map_image_path: str = "assets/mapav4.png"
    create_grid_from_img: bool = True
    target: Coords = (6, 31)
    source: Coords = (6, 15)

@dataclass
class PopulationSettings:
    """
    Simulation metadata and other implementation details.

    Attributes:
        spawn_interval: The interval at which new ants are spawned.
        time_to_spawn: The time remaining until the next spawn.

    """
    spawn_interval: int = 30
    time_to_spawn: int = 0





@dataclass
class SimulationSettings:
    """
    Simulation settings for the fox model.

    Attributes:
        generic: Simulation parameters related to implementation details.
    """
    generic: GenericSimulationSettings
    population: PopulationSettings


def get_default_simulation_settings() -> SimulationSettings:
    """
    Get the default settings for the fox model.

    Returns:
        The default settings.
    """
    return SimulationSettings(
        generic=GenericSimulationSettings(),
        population=PopulationSettings(),
    )
