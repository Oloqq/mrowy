from dataclasses import dataclass, field
from enum import Enum


class TimeStep(int, Enum):
    HOURLY = 1
    EVERY_2_HOURS = 2
    EVERY_3_HOURS = 3
    DAY_PART = 4


class DistributionType(int, Enum):
    UNIFORM = 1
    NORMAL = 2
    EXPONENTIAL = 3


class Sex(int, Enum):
    MALE = 1
    FEMALE = 2


@dataclass
class MinMaxRandomValue:
    """
    Type of randomly generated value with a min and max.

    Attributes:
        min: The minimum value.
        max: The maximum value.
        distribution_type: The distribution type.
        distribution_params: The distribution parameters.
    """
    min: float
    max: float
    distribution_type: DistributionType
    distribution_params: dict[str, float]


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
class HomeRangeSettings:
    """"
    Settings related to the home range of the foxes (local areas in which they hunt).

    Attributes:
        size: The size of the home range.
        birth_period_size: Smaller range size after birth of new foxes.
        avg_eccentricity: The average eccentricity of the home range (it is elliptical).
        std_eccentricity: The standard deviation of the eccentricity of the home range.
    """

    size: MinMaxRandomValue = MinMaxRandomValue(0.8, 8.0, DistributionType.NORMAL, {"avg": 2, "stddev": 0.5})
    birth_period_size: MinMaxRandomValue = MinMaxRandomValue(0.2, 2.0, DistributionType.NORMAL, {"avg": 0.8, "stddev": 0.2})

    avg_eccentricity: float = 0.5
    std_eccentricity: float = 0.1


@dataclass
class ReproductionSettings:
    """
    Settings related to the reproduction of the foxes.

    Attributes:
        cubs_per_litter: The number of cubs per litter.
        length_of_gestation: The length of the gestation period.
        sexual_maturity_age: The age at which the foxes become sexually mature.
        birth_rate_period: Days of the year in which the birth is more likely to occur.
    """

    cubs_per_litter: MinMaxRandomValue = MinMaxRandomValue(3, 17, DistributionType.EXPONENTIAL, {"lambda": 0.2})
    length_of_gestation: MinMaxRandomValue = MinMaxRandomValue(50, 52, DistributionType.UNIFORM, {})
    sexual_maturity_age: MinMaxRandomValue = MinMaxRandomValue(9, 10, DistributionType.UNIFORM, {})
    birth_rate_period: tuple[int, int] = (0, 31 + 28)


@dataclass
class MortalitySettings:
    """
    Settings related to the mortality of the foxes.

    Attributes:
        mortality_rate: The mortality rate of the foxes (chance of dying in a specific year).
    """

    mortality_rate: MinMaxRandomValue = MinMaxRandomValue(0.05, 0.32, DistributionType.UNIFORM, {})


@dataclass
class DispersalSettings:
    """
    Settings related to the dispersal of the foxes.

    Attributes:
        dispersal_age: Minimum age at which the foxes disperse.
        dispersal_distance: The distance the foxes disperse for each sex.
        dispersal_start: The start of the dispersal period (day of the year).
        dispersal_end: The end of the dispersal period (day of the year).
    """

    dispersal_age: float = 0.5
    dispersal_distance: dict[Sex, MinMaxRandomValue] = field(default_factory=lambda: {
        Sex.MALE: MinMaxRandomValue(5, 122, DistributionType.NORMAL, {"avg": 29, "stddev": 10}),
        Sex.FEMALE: MinMaxRandomValue(2, 24, DistributionType.NORMAL, {"avg": 12, "stddev": 4}),
    })
    dispersal_start: int = 9.5 * 30
    dispersal_end: int = 3 * 30


@dataclass
class ShootingSettings:
    """
    Settings related to the shooting of the foxes.

    Attributes:
        culling_rate: The rate at which the foxes are culled (their mother is killed at the den).
        shooting_rate: Number of foxes shot per a single excursion.
        shooting_excursions: Number of excursions per year on simulation terrain.
    """

    culling_rate: MinMaxRandomValue = MinMaxRandomValue(1, 30, DistributionType.NORMAL, {"avg": 10, "stddev": 5})
    shooting_rate: MinMaxRandomValue = MinMaxRandomValue(0, 2, DistributionType.NORMAL, {"avg": 0.5, "stddev": 0.2})
    shooting_excursions: MinMaxRandomValue = MinMaxRandomValue(10, 80, DistributionType.NORMAL, {"avg": 30, "stddev": 10})
    shooting_start: int = 6 * 30
    shooting_end: int = 3 * 30


@dataclass
class SocialSettings:
    """
    Settings related to the social behaviour of the foxes.

    Attributes:
        social_group_size: The size of the social group of the foxes.
    """

    social_group_size: MinMaxRandomValue = MinMaxRandomValue(2, 5, DistributionType.NORMAL, {"avg": 3, "stddev": 1})


@dataclass
class MovementSettings:
    """
    Settings related to the movement of the foxes.

    Attributes:
        normal_speed: The normal speed of the foxes.
        max_speed: The maximum speed of the foxes.
    """

    normal_speed: int = 7
    max_speed: int = 45


@dataclass
class FoxSimulationSettings:
    """
    Settings related to the foxes.

    Attributes:
        home_range: Settings related to the home range of the foxes.
        reproduction: Settings related to the reproduction of the foxes.
        mortality: Settings related to the mortality of the foxes.
        dispersal: Settings related to the dispersal of the foxes.
        social: Settings related to the social behaviour of the foxes.
        movement: Settings related to the movement of the foxes.
    """
    home_range: HomeRangeSettings
    reproduction: ReproductionSettings
    mortality: MortalitySettings
    dispersal: DispersalSettings
    shooting: ShootingSettings
    social: SocialSettings
    movement: MovementSettings


@dataclass
class SimulationSettings:
    """
    Simulation settings for the fox model.

    Attributes:
        generic: Simulation parameters related to implementation details.
    """
    generic: GenericSimulationSettings
    fox: FoxSimulationSettings


def get_default_settings() -> SimulationSettings:
    """
    Get the default settings for the fox model.

    Returns:
        The default settings.
    """
    return SimulationSettings(
        generic=GenericSimulationSettings(),
        fox=FoxSimulationSettings(
            home_range=HomeRangeSettings(),
            reproduction=ReproductionSettings(),
            mortality=MortalitySettings(),
            dispersal=DispersalSettings(),
            shooting=ShootingSettings(),
            social=SocialSettings(),
            movement=MovementSettings()
        )
    )