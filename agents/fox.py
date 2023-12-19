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
    normal_distribution_settings: MinMaxRandomValue

    def __init__(self, fox_settings: FoxSimulationSettings, sex: Sex, den_position: tuple[int, int]):
        self.settings = fox_settings
        self.age = 0
        self.sex = sex
        self.den_position = Vector2(den_position)
        self.current_position = Vector2(den_position)
        self.home_range = self.generate_home_range()
        # basic configuration to get random value
        self.normal_distribution_settings = MinMaxRandomValue(min=-1.5*self.settings.movement.normal_speed, max=1.5*self.settings.movement.normal_speed,
                                                              distribution_type=DistributionType.NORMAL,
                                                              distribution_params={"avg": 0, "stddev": 1})

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

    def move(self):
        # foxes move in random direction, with random value from normal distribution,
        # taking into account their normal speed
        random_value_x = self.normal_distribution_settings.get_random_value()
        random_value_y = self.normal_distribution_settings.get_random_value()
        new_x = int(self.current_position.x + random_value_x)
        new_y = int(self.current_position.y + random_value_y)

        # if new position is out of home range - fox doesnt move - temporary solution
        if (new_x, new_y) not in self.home_range:
            pass
        else:
            self.current_position = Vector2(new_x, new_y)
