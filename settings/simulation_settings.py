from constants.enums import TimeStep
from dataclasses import dataclass
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
    duration: int = 100
    map_image_path: str = "assets/mapav5.png"
    create_grid_from_img: bool = True
    simple_map: bool = False
    target: Coords = (6, 31)
    source: Coords = (6, 15)
    # TODO find optimal settings
    node_capacity: int = 1
    node_max_smell: float = 100.0


@dataclass
class PopulationSettings:
    """
    Simulation metadata and other implementation details.

    Attributes:
        spawn_interval: The interval at which new ants are spawned.
        time_to_spawn: The time remaining until the next spawn.

    """
    time_to_spawn: int = 0
    ant_max_memory: int = 3000
    opulation_size: int = 100

    # TODO bind to distance
    # propozycja:
    # jeśli dystans bezwzględny między polami (oś x + oś y) wynosi 0 < x < 100 to wartości np (do sprawdzenia):
    # spawn_interval: int = 300
    # pheromone_decay: float = 1
    # destination_bonus: float = 20.0

    # 100 < x < 200
    # spawn_interval: int = 1000
    # pheromone_decay: float = 0.5
    # destination_bonus: float = 30.0

    # 200 < x < 300
    # spawn_interval: int = 2500
    # pheromone_decay: float = 0.3
    # destination_bonus: float = 30.0

    # 200 < x < 300
    # spawn_interval: int = 4000
    # pheromone_decay: float = 0.3
    # destination_bonus: float = 30.0

    destination_bonus: float = 30.0
    spawn_interval: int = 4000
    pheromone_decay: float = 0.3


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
