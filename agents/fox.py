import random
import math

from pygame import Vector2

from framework.min_max_random_value import MinMaxRandomValue
from settings.simulation_settings import FoxSimulationSettings
from constants.enums import Sex, DistributionType, ObjectType, FieldType
from settings.pg_settings import PygameSettings
from collections import deque


class Fox:
    age: int
    sex: Sex
    den_position: Vector2
    current_position: Vector2
    low_activity_distribution_settings: MinMaxRandomValue
    high_activity_distribution_settings: MinMaxRandomValue
    hunger: float
    hunger_increase_per_hour: float

    def __init__(self, fox_settings: FoxSimulationSettings, sex: Sex, den_position: Vector2,
                 population_manager, date):
        self.population_manager = population_manager
        self.settings = fox_settings
        #TODO:
        # if foxes can only get pregnant during january/february, then we can't randomly have a fox with age 4 months
        # during january, because that's impossible. so we need to randomize the age of initial population in some clever way I guess
        self.age = 11  # age in months. set to 11 for testing reproduction - we can randomize it for initial population not to start with 0
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
        self.high_activity_distribution_settings = self.settings.movement.default_high_activity_speed()
        self.mortality_rate = self.settings.mortality.default_mortality_rate().get_random_value()
        self.maturity_age = self.settings.reproduction.default_sexual_maturity_age().get_random_value()
        self.birth_period = self.settings.reproduction.birth_rate_period
        self.day_of_death = self.set_death_date(date)
        self.dispersal_distance = self.settings.dispersal.dispersal_distance[self.sex].get_random_value()
        self.dispersal_day = int((285 + self.settings.dispersal.default_dispersal_day().get_random_value())) % 365 + 1
        #TODO:
        # if age higher than dispersal age, set to true
        self.has_dispersed = False

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

        # Calculate legal postions (Fox can't go through water)
        legal_positions = []
        starting_position = self.den_position
        positions_to_check = [(int(self.den_position.x), int(self.den_position.y))]
        checked = {}
        while len(positions_to_check) > 0:
            position = positions_to_check.pop()
            if position[0] < 0 or position[0] >= self.population_manager.grid.shape[0] or position[1] < 0 or \
                    position[1] >= self.population_manager.grid.shape[1]:
                continue
            checked[position] = True
            if self.population_manager.grid[position] != FieldType.WATER:
                legal_positions.append(position)
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        new_position = (position[0] + x, position[1] + y)
                        if new_position not in checked and new_position not in positions_to_check:
                            positions_to_check.append(new_position)

        return list(set(home_range) & set(legal_positions))

    def set_death_date(self, date):
        year = 1
        while True:
            if random.random() < self.mortality_rate + ((self.age/12 + year) / 25) or self.age/12 + year == 14: 
                day = random.randint(1, 365)
                hour = random.randint(0, 23)
                return year+int(date.year), day, hour
            else:
                year += 1
                

    def move(self, date, objects, food_matrix):
        # Aktywność przy padlinie jest skoncentrowana głównie w godzinach 0:00 -
        # 3:00 i 18:00 - 22:00, podobnie jak czas spędzany przy punktach wodnych, który przeważnie występuje w
        # godzinach 03:00 - 06:00 i 20:00 - 23:00. W przypadku nor króliczych, lisy najczęściej obserwuje się w
        # okolicach tych miejsc między godzinami 19:00 a 22:00.

        # 0:00 - 3:00 i 18:00 - 22:00 - szukaj jedzenia
        # 19:00 - 22:00 - poluj na króliki
        
        if 19 <= date.hour < 22:
            self.hunt_rabbits(objects)
        if 0 <= date.hour < 3 or 18 <= date.hour < 22:
            self.search_for_food(food_matrix)

        self.change_position(date.hour)
        self.increase_hunger()
        self.check_death(date)

        # Age
        if date.month == 1 and date.day == 1 and date.hour == 1:
            self.age += 1
            self.was_pregnant_this_year = False
            self.mortality_rate = self.settings.mortality.mortality_rate.get_random_value()

        # Reproduction
        #TODO: add some randomness, so that foxes don't reproduce at the same time
        if self.sex == Sex.FEMALE and (date.month == 1 or date.month == 2) and self.age >= self.maturity_age \
                and self.was_pregnant_this_year is False and self.is_pregnant is False:
            self.search_for_mate()
        
        # Dispersal
        if date.timetuple().tm_yday == self.dispersal_day and not self.has_dispersed:
            self.disperse(objects, date)

        # Count days until birth
        if date.hour == 0 and self.is_pregnant is True:
            if self.days_till_birth > 0:
                self.days_till_birth -= 1
            else:
                self.birth(date)

    def change_position(self, hour):
        return_to_den = False
        distribution_settings = self.low_activity_distribution_settings
        if 6 > hour or hour > 18:  # most active
            distribution_settings = self.high_activity_distribution_settings
        elif random.random() < 0.8:
            return_to_den = True

        if return_to_den:
            self.current_position = self.den_position
            return

        # If current position is too far from den, fox moves back to home range (occasional ventures are permitted)
        if self.current_position not in self.home_range:
            if len(self.home_range) == 0:
                return
            new_x, new_y = min(self.home_range, key=lambda pos: (pos[0] - self.current_position.x) ** 2 +
                                                                (pos[1] - self.current_position.y) ** 2)
            self.current_position = Vector2(new_x, new_y)
            return

        random_value_x = distribution_settings.get_random_value()
        random_value_y = distribution_settings.get_random_value()
        new_x = int(self.current_position.x + random_value_x)
        new_y = int(self.current_position.y + random_value_y)

        if self.population_manager.grid.shape[0] <= new_x or self.population_manager.grid.shape[1] <= new_y or new_x < 0 \
                or new_y < 0 or self.population_manager.grid[new_x, new_y] == FieldType.WATER:
            return

        self.current_position = Vector2(new_x, new_y)

    def feed(self, value):
        if self.hunger < value:
            self.hunger = 0
        else:
            self.hunger -= value

    def increase_hunger(self):
        self.hunger += self.hunger_increase_per_hour

    def hunt_rabbits(self, objects):
        grid_size = PygameSettings.GRID_WIDTH, PygameSettings.GRID_HEIGHT
        # function checks if there is a rabbit den in 5x5 surrounding of fox - if there is, fox feeds on it
        for x in range(int(max(0, self.current_position.x - 2)), int(min(grid_size[0], self.current_position.x + 3))):
            for y in range(int(max(0, self.current_position.y - 2)), int(min(grid_size[1], self.current_position.y + 3))):
                if objects[x, y] is ObjectType.RABBIT_DEN:
                    chance = random.random()
                    if chance < 0.6 and self.population_manager.grid[x, y] == FieldType.GRASS:
                        self.feed(1)
                    elif chance < 0.8 and self.population_manager.grid[x, y] == FieldType.FOREST:
                        self.feed(1)
                    return

    def search_for_food(self, food_matrix):
        pos_x = max(min(int(self.current_position.x), food_matrix.shape[0] - 1), 0)
        pos_y = max(min(int(self.current_position.y), food_matrix.shape[1] - 1), 0)
        pos = (pos_x, pos_y)

        food_amount = food_matrix[pos]
        if food_amount < 0.5:
            self.feed(food_amount)
            food_matrix[pos] = 0
        else:
            self.feed(0.5)
            food_matrix[pos] -= 0.5


    def check_death(self, date):
        if self.hunger > 1:
            self.population_manager.remove_fox(self)
            print("Fox died of hunger")
        if self.day_of_death is not None and date.year == self.day_of_death[0] and date.timetuple().tm_yday == self.day_of_death[1] and date.hour == \
                self.day_of_death[2]:
            self.population_manager.remove_fox(self)
            print("Fox died of natural reasons")

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

    def birth(self, date):
        self.is_pregnant = False
        self.population_manager.add_foxes(self, self.settings.reproduction.default_cubs_per_litter().get_random_value(), date)

    def reproduce(self):
        self.is_pregnant = True
        self.was_pregnant_this_year = True
        self.days_till_birth = self.settings.reproduction.default_length_of_gestation().get_random_value()

    def disperse(self, objects, date):
        grid_size = PygameSettings.GRID_WIDTH, PygameSettings.GRID_HEIGHT

        # find dens in dispersal distance
        queue = deque([(int(self.current_position.x), int(self.current_position.y))])
        checked = set()
        dens = []

        while queue:
            position = queue.popleft()
            if position in checked:
                continue
            checked.add(position)
            if self.population_manager.grid[position] == FieldType.WATER:
                continue
            for x in range(int(max(0, position[0] - 1)), int(min(grid_size[0], position[0] + 2))):
                for y in range(int(max(0, position[1] - 1)), int(min(grid_size[1], position[1] + 2))):
                    queue.append((x, y))
            distance = math.sqrt((position[0] - int(self.den_position.x))**2 + (position[1] - int(self.den_position.y))**2)
            if distance > self.dispersal_distance:
                continue
            if objects[position[0], position[1]] == ObjectType.FOX_DEN and (position[0], position[1]) != (self.den_position.x, self.den_position.y):
                dens.append((position, distance))

        # choose one by random, weighted by their distance (further = less likely)
        weights = [1 / distance for _, distance in dens]
        # temp = self.den_position
        self.den_position = Vector2(random.choices(dens, weights=weights)[0][0]) if len(dens) > 0 else self.den_position
        # print("Fox dispersed from ", temp, " to", self.den_position, ", distance ", distance, "Dispersal age: ", self.dispersal_day, "Current day: ", date.timetuple().tm_yday)
        self.has_dispersed = True

        return