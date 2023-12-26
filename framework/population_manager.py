from settings.simulation_settings import SimulationSettings, FoxSimulationSettings
from dataclasses import dataclass
from constants.enums import Sex
from agents.fox import Fox
import random


@dataclass
class PopulationSettings:
    INITIAL_POPULATION_SIZE: int = 100


def get_default_population_settings() -> PopulationSettings:
    return PopulationSettings()


class FoxGroup:
    def __init__(self, group_id: int, den_position: tuple[int, int], fox_settings: FoxSimulationSettings):
        self.group_id = group_id
        self.size = int(fox_settings.social.social_group_size.get_random_value())
        dominant_male = Fox(fox_settings, Sex.MALE, den_position)
        dominant_female = Fox(fox_settings, Sex.FEMALE, den_position)
        self.foxes = [dominant_male, dominant_female]

        for i in range(self.size - 2):
            self.foxes.append(Fox(fox_settings, Sex.MALE if random.random() > 0.5 else Sex.FEMALE, den_position))

    def __repr__(self):
        str_repr = f"------- Group {self.group_id} -------\n"
        str_repr += f"Size: {self.size}\n"
        str_repr += f"Den position: {self.foxes[0].den_position}\n"
        for fox in self.foxes:
            str_repr += f"{fox}\n"
        return str_repr


class PopulationManager:

    def __init__(self, simulation_settings: SimulationSettings):
        self.groups = []
        self.simulation_settings = simulation_settings
        self.settings = get_default_population_settings()

    def create_population(self, den_positions: list[tuple[int, int]]):
        for i, den_position in enumerate(den_positions):
            self.groups.append(FoxGroup(i, den_position, self.simulation_settings.fox))

    def get_foxes(self):
        foxes = []
        for group in self.groups:
            foxes.extend(group.foxes)
        return foxes

    def remove_fox(self, fox: Fox):
        for group in self.groups:
            if fox in group.foxes:
                group.foxes.remove(fox)
                group.size -= 1
                if group.size == 0:
                    self.groups.remove(group)
                break

    def add_foxes(self, fox: Fox, number_of_cubs):
        for group in self.groups:
            if fox in group.foxes:
                for i in range(int(number_of_cubs)):
                    child = Fox(self.simulation_settings.fox,
                        Sex.MALE if random.random() > 0.5 else Sex.FEMALE, fox.den_position)
                    child.age = 0
                    group.foxes.append(child)
                break
