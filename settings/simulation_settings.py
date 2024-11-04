from constants.enums import DistributionType, TimeStep, Sex
from dataclasses import dataclass, field


@dataclass
class GenericSimulationSettings:
    """
    Simulation metadata and other implementation details.

    Attributes:
        grid_size: The size of the grid in (x, y) format.
        tile_size: The size of a single tile in the grid in meters.
        time_step: The time step of the simulation.
        duration: The duration of the simulation in time steps.
    """

    grid_size: tuple[int, int] = (100, 100)
    time_step: TimeStep = TimeStep.HOURLY
    tile_size: int = 1
    duration: int = 1000

@dataclass
class SimulationSettings:
    """
    Simulation settings for the fox model.

    Attributes:
        generic: Simulation parameters related to implementation details.
    """
    generic: GenericSimulationSettings


def get_default_simulation_settings() -> SimulationSettings:
    """
    Get the default settings for the fox model.

    Returns:
        The default settings.
    """
    return SimulationSettings(
        generic=GenericSimulationSettings(),
    )
