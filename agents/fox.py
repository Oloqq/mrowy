import random

from pygame import Vector2

from framework.min_max_random_value import MinMaxRandomValue
from settings.simulation_settings import FoxSimulationSettings
from constants.enums import Sex, DistributionType, ObjectType


class Fox:
    age: int
    sex: Sex
    den_position: Vector2
    current_position: Vector2
    low_activity_distribution_settings: MinMaxRandomValue
    high_activity_distribution_settings: MinMaxRandomValue
    hunger: float
    hunger_increase_per_hour: float

    def __init__(self, fox_settings: FoxSimulationSettings, sex: Sex, den_position: tuple[int, int],
                 population_manager):
        self.population_manager = population_manager
        self.settings = fox_settings
        self.age = 11  # for testing reproduction - we can randomize it for initial population not to start with 0
        self.sex = sex
        self.hunger = 0
        self.hunger_increase_per_hour = fox_settings.mortality.hunger_increase_per_hour
        self.den_position = Vector2(den_position)
        self.current_position = Vector2(den_position)
        self.home_range = self.generate_home_range()
        self.is_pregnant = False
        self.was_pregnant_this_year = False
        self.days_till_birth = 0
        self.low_activity_distribution_settings = self.settings.movement.default_low_activity_speed()
        self.high_activity_distribution_settings = self.settings.movement.defautl_high_activity_speed()
        self.mortality_rate = self.settings.mortality.default_mortality_rate().get_random_value()
        self.maturity_age = self.settings.reproduction.default_sexual_maturity_age().get_random_value()
        self.birth_period = self.settings.reproduction.birth_rate_period
        self.day_of_death = self.set_death_date()

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

    def set_death_date(self):
        if random.random() < self.mortality_rate + (self.age / 100):
            date = random.randint(1, 365)
            hour = random.randint(0, 23)
            return date, hour
        else:
            return None

    def move(self, population_manager, date, objects, food_matrix):
        # Aktywność przy padlinie jest skoncentrowana głównie w godzinach 0:00 -
        # 3:00 i 18:00 - 22:00, podobnie jak czas spędzany przy punktach wodnych, który przeważnie występuje w
        # godzinach 03:00 - 06:00 i 20:00 - 23:00. W przypadku nor króliczych, lisy najczęściej obserwuje się w
        # okolicach tych miejsc między godzinami 19:00 a 22:00.
        if 19 < date.hour < 22:
            self.hunt_rabbits(objects)
        if 0 < date.hour < 3 or 18 < date.hour < 22:
            self.search_for_food(food_matrix)

        self.change_position(date.hour)
        self.increase_hunger()
        self.check_death(date)

        if date.month == 1 and date.day == 1 and date.hour == 1:
            self.age += 1
            self.was_pregnant_this_year = False
            self.mortality_rate = self.settings.mortality.mortality_rate.get_random_value()

        if self.sex == Sex.FEMALE and (date.month == 1 or date.month == 2) and self.age >= self.maturity_age \
                and self.was_pregnant_this_year is False and self.is_pregnant is False:
            self.search_for_mate()

        if date.hour == 0 and self.is_pregnant is True:
            if self.days_till_birth > 0:
                self.days_till_birth -= 1
            else:
                self.birth()

    def change_position(self, hour):
        if 6 > hour or hour > 18:  # most active
            distribution_settings = self.high_activity_distribution_settings
        else:
            distribution_settings = self.low_activity_distribution_settings

        random_value_x = distribution_settings.get_random_value()
        random_value_y = distribution_settings.get_random_value()
        new_x = int(self.current_position.x + random_value_x)
        new_y = int(self.current_position.y + random_value_y)
        # if new position is too far from den - fox moves to the closest position in home range - temporary solution
        if (new_x - self.den_position.x) ** 2 + (new_y - self.den_position.y) ** 2 > 5 ** 2:
            new_x, new_y = min(self.home_range, key=lambda pos: (pos[0] - new_x) ** 2 + (pos[1] - new_y) ** 2)
        self.current_position = Vector2(new_x, new_y)

    def feed(self, value):
        if self.hunger < value:
            self.hunger = 0
        else:
            self.hunger -= value

    def increase_hunger(self):
        self.hunger += self.hunger_increase_per_hour

    def hunt_rabbits(self, objects):
        # function checks if there is a rabbit den in 5x5 surrounding of fox - if there is, fox feeds on it
        for x in range(int(max(0, self.current_position.x - 2)), int(min(30, self.current_position.x + 3))):
            for y in range(int(max(0, self.current_position.y - 2)), int(min(50, self.current_position.y + 3))):
                if objects[x, y] is ObjectType.RABBIT_DEN:
                    self.feed(1)
                    return

    def search_for_food(self, food_matrix):
        self.feed(food_matrix[
                      min(int(self.current_position.x), food_matrix.shape[0] - 1), min(int(self.current_position.y),
                                                                                       food_matrix.shape[1] - 1)])

    def check_death(self, date):
        if self.hunger > 1:
            self.population_manager.remove_fox(self)
            print("fox died of hunger")
        if self.day_of_death is not None and date.timetuple().tm_yday == self.day_of_death[0] and date.hour == \
                self.day_of_death[1]:
            self.population_manager.remove_fox(self)
            print("fox died of natural reasons")

    def search_for_mate(self):
        # if there is a den and a male in 3x3 square, they mate
        if abs(self.current_position.x - self.den_position.x) >= 2 and abs(
                self.current_position.y - self.den_position.y) >= 2:
            return
        foxes = filter(lambda fox: fox.sex == Sex.MALE, self.population_manager.get_foxes())
        for fox in foxes:
            if abs(fox.current_position.x - self.current_position.x) < 2 and abs(
                    fox.current_position.y - self.current_position.y) < 2:
                self.reproduce()
                break

    def birth(self):
        self.is_pregnant = False
        self.population_manager.add_foxes(self, self.settings.reproduction.default_cubs_per_litter().get_random_value())

    def reproduce(self):
        self.is_pregnant = True
        self.was_pregnant_this_year = True
        self.days_till_birth = self.settings.reproduction.default_length_of_gestation().get_random_value()
