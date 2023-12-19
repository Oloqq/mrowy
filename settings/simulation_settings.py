from framework.min_max_random_value import MinMaxRandomValue
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
class HomeRangeSettings:
    """"
    Settings related to the home range of the foxes (local areas in which they hunt).

    Attributes:
        size: The size of the home range.
        birth_period_size: Smaller range size after birth of new foxes.
        radius_ratio: The average eccentricity of the home range (it is elliptical).
        std_radius_ratio: The standard deviation of the eccentricity of the home range.
    """

    @staticmethod
    def default_size():
        return MinMaxRandomValue(0.8, 8.0, DistributionType.NORMAL, {"avg": 3, "stddev": 0.5})

    @staticmethod
    def default_birth_period_size():
        return MinMaxRandomValue(0.2, 2.0, DistributionType.NORMAL, {"avg": 0.8, "stddev": 0.2})

    @staticmethod
    def default_radius_ratio():
        return MinMaxRandomValue(0.5, 1.0, DistributionType.UNIFORM, {})

    size: MinMaxRandomValue = field(default_factory=default_size)
    birth_period_size: MinMaxRandomValue = field(default_factory=default_birth_period_size)
    radius_ratio: MinMaxRandomValue = field(default_factory=default_radius_ratio)


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

    @staticmethod
    def default_cubs_per_litter():
        return MinMaxRandomValue(3, 17, DistributionType.EXPONENTIAL, {"lambda": 0.2})

    @staticmethod
    def default_length_of_gestation():
        return MinMaxRandomValue(50, 52, DistributionType.UNIFORM, {})

    @staticmethod
    def default_sexual_maturity_age():
        return MinMaxRandomValue(9, 10, DistributionType.UNIFORM, {})

    cubs_per_litter: MinMaxRandomValue = field(default_factory=default_cubs_per_litter)
    length_of_gestation: MinMaxRandomValue = field(default_factory=default_length_of_gestation)
    sexual_maturity_age: MinMaxRandomValue = field(default_factory=default_sexual_maturity_age)
    birth_rate_period: tuple[int, int] = (0, 31 + 28)


@dataclass
class MortalitySettings:
    """
    Settings related to the mortality of the foxes.

    Attributes:
        mortality_rate: The mortality rate of the foxes (chance of dying in a specific year).
    """

    @staticmethod
    def default_mortality_rate():
        return MinMaxRandomValue(0.05, 0.32, DistributionType.UNIFORM, {})

    mortality_rate: MinMaxRandomValue = field(default_factory=default_mortality_rate)
    hunger_increase_per_hour: float = 0.02


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

    @staticmethod
    def default_culling_rate():
        return MinMaxRandomValue(1, 30, DistributionType.NORMAL, {"avg": 10, "stddev": 5})

    @staticmethod
    def default_shooting_rate():
        return MinMaxRandomValue(0, 2, DistributionType.NORMAL, {"avg": 0.5, "stddev": 0.2})

    @staticmethod
    def default_shooting_excursions():
        return MinMaxRandomValue(10, 80, DistributionType.NORMAL, {"avg": 30, "stddev": 10})

    culling_rate: MinMaxRandomValue = field(default_factory=default_culling_rate)
    shooting_rate: MinMaxRandomValue = field(default_factory=default_shooting_rate)
    shooting_excursions: MinMaxRandomValue = field(default_factory=default_shooting_excursions)
    shooting_start: int = 6 * 30
    shooting_end: int = 3 * 30


@dataclass
class SocialSettings:
    """
    Settings related to the social behaviour of the foxes.

    Attributes:
        social_group_size: The size of the social group of the foxes.
    """

    @staticmethod
    def default_social_group_size():
        return MinMaxRandomValue(2, 5, DistributionType.NORMAL, {"avg": 3, "stddev": 1})

    social_group_size: MinMaxRandomValue = field(default_factory=default_social_group_size)


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


def get_default_simulation_settings() -> SimulationSettings:
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
