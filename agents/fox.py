from pygame import Vector2

from settings.simulation_settings import FoxSimulationSettings
from constants.enums import Sex


class Fox:
    age: int
    sex: Sex
    den_position: Vector2
    current_position: Vector2

    def __init__(self, fox_settings: FoxSimulationSettings, sex: Sex, den_position: tuple[int, int]):
        self.settings = fox_settings
        self.age = 0
        self.sex = sex
        self.den_position = Vector2(den_position)
        self.current_position = Vector2(den_position)

    def
