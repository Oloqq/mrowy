import random

from pygame import Vector2

from framework.min_max_random_value import MinMaxRandomValue
from settings.simulation_settings import FoxSimulationSettings
from constants.enums import Sex, DistributionType


class Fox:
    age: int
    sex: Sex
    den_position: Vector2
    current_position: Vector2
    low_activity_distribution_settings: MinMaxRandomValue
    high_activity_distribution_settings: MinMaxRandomValue

    def __init__(self, fox_settings: FoxSimulationSettings, sex: Sex, den_position: tuple[int, int]):
        self.settings = fox_settings
        self.age = 0
        self.sex = sex
        self.den_position = Vector2(den_position)
        self.current_position = Vector2(den_position)
        self.home_range = self.generate_home_range()
        # basic configuration to get random value
        self.low_activity_distribution_settings = MinMaxRandomValue(min=-1.5 * self.settings.movement.normal_speed,
                                                                    max=1.5 * self.settings.movement.normal_speed,
                                                                    distribution_type=DistributionType.NORMAL,
                                                                    distribution_params={"avg": 0, "stddev": 1})
        self.high_activity_distribution_settings = MinMaxRandomValue(min=-1.5 * self.settings.movement.normal_speed,
                                                                      max=1.5 * self.settings.movement.normal_speed,
                                                                      distribution_type=DistributionType.NORMAL,
                                                                      distribution_params={"avg": 0, "stddev": 0.3})

    def generate_home_range(self):
        home_range_settings = self.settings.home_range
        home_range = []

        h, k = self.den_position

        home_range_radius = int(home_range_settings.size.get_random_value())
        home_range_ratio = home_range_settings.radius_ratio.get_random_value()

        small_radius = int(home_range_radius / (1 / 2 + home_range_ratio))

        if small_radius == 0:
            small_radius = 1

        large_radius = int(small_radius / home_range_ratio)

        if random.random() > 0.5:
            small_radius, large_radius = large_radius, small_radius

        for x in range(-small_radius, small_radius + 1):
            for y in range(-large_radius, large_radius + 1):
                if x ** 2 / small_radius ** 2 + y ** 2 / large_radius ** 2 <= 1:
                    home_range.append((int(x + h), int(y + k)))

        return home_range

    def move(self, hour):
        # Najczęściej lisy zdobywają zasoby między godzinami 6:00 a 18:00,
        # choć konkretne źródła pożywienia sprawdzają w nieco różnych porach.
        # Aktywność przy padlinie jest skoncentrowana głównie w godzinach 0:00 - 3:00 i 18:00 - 22:00,
        # podobnie jak czas spędzany przy punktach wodnych,
        # który przeważnie występuje w godzinach 03:00 - 06:00 i 20:00 - 23:00.
        # W przypadku nor króliczych, lisy najczęściej obserwuje się w okolicach tych miejsc między godzinami 19:00 a 22:00.

        if 6 < hour < 18:  #most active
            distribution_settings = self.high_activity_distribution_settings
        else:
            distribution_settings = self.low_activity_distribution_settings

        random_value_x = distribution_settings.get_random_value()
        random_value_y = distribution_settings.get_random_value()
        new_x = int(self.current_position.x + random_value_x)
        new_y = int(self.current_position.y + random_value_y)

        # if new position is out of home range - fox moves to closest position in home range - temporary solution
        if (new_x, new_y) not in self.home_range:
            new_x, new_y = min(self.home_range, key=lambda pos: (pos[0] - new_x) ** 2 + (pos[1] - new_y) ** 2)

        self.current_position = Vector2(new_x, new_y)



