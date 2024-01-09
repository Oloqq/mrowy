import random
import math

from pygame import Vector2

from framework.min_max_random_value import MinMaxRandomValue
from settings.simulation_settings import ShootingSettings
from settings.pg_settings import PygameSettings
from constants.enums import FieldType, ObjectType

class Hunter:
    current_position: Vector2
    culling_rate: MinMaxRandomValue
    shooting_rate: MinMaxRandomValue
    shooting_excursions: MinMaxRandomValue
    available_positions: list[Vector2]

    def __init__(self, shooting_settings: ShootingSettings, population_manager, objects):
        self.population_manager = population_manager
        self.settings = shooting_settings
        self.range = 3 # n in every direction, so (n+1)x(n+1) area
        self.available_positions = self.find_available_positions(objects)
        self.position = random.choice(self.available_positions)
        self.culling_rate = shooting_settings.default_culling_rate().get_random_value()
        self.shooting_rate = shooting_settings.default_shooting_rate().get_random_value()
        # this will be generated at the beggining of simulation, the very first time hunt() is called        
        self.shooting_days = []
    
# Zresp sobie huntera w jakimś miejscu
# Poluje self.shooting_excursions razy w roku, zabijając self.shooting_rate lisów
# self.culling_rate szansy na zabicie matki w norze?? 
# Będzie skanował teren 7x7 wokół siebie i wymiatał lisy z tego terenu, jeśli nie ma to im się farci albo coś idk
# Po zakończeniu polowania przerzuć się do losowej innej pozycji na mapie (ale najlepiej w stronę lisów)
# Po zakończeniu polowania zaktualizuj self.culling_rate i self.shooting_rate
# Po zakończeniu sezonu polowania zaktualizuj self.shooting_excursions
    
    # Find every good hunting position (has to be near fox dens and not in water)
    def find_available_positions(self, objects):
        available_positions = []
        for x in range(self.population_manager.grid.shape[0]):
            for y in range(self.population_manager.grid.shape[1]):
                if self.population_manager.grid[x][y] != FieldType.WATER:
                    #iterate over all positions in a (n+1)x(n+1) [n = range] square around the hunter and look for fox dens
                    if self.look_for_den(x, y, objects):
                        available_positions.append((x,y))
        return available_positions
    
    def look_for_den(self, x, y, objects):
        for i in range(-self.range, self.range+1):
            for j in range(-self.range, self.range+1):
                if x+i >= 0 and x+i < objects.shape[0] and y+j >= 0 and y+j < objects.shape[1]:
                    if objects[x+i][y+j] == ObjectType.FOX_DEN:
                        return True
        return False

    # Create a list of hunting days
    def generate_shooting_array(self):
        # Generate an array of all legal hunting days
        legal_shooting_days = []
        for i in range(1, self.settings.shooting_end+1):
            legal_shooting_days.append(i)
        for i in range(self.settings.shooting_start, 366):
            legal_shooting_days.append(i)

        # hunting_amount = int(self.settings.default_shooting_excursions().get_random_value())
        hunting_amount = 60
        shooting_days = random.sample(legal_shooting_days, hunting_amount)
        self.shooting_days = sorted(shooting_days)
        print(f"Hunting days:\n {self.shooting_days}")

    def hunt(self, date, foxes):
        if date.timetuple().tm_yday == 1:
            self.generate_shooting_array()
        # Check if it's a hunting day
        if date.timetuple().tm_yday not in self.shooting_days:
            return
        self.shooting_days.remove(date.timetuple().tm_yday)

        # Check how many foxes killed
        foxes_killed = round(self.settings.default_shooting_rate().get_random_value())
        if foxes_killed == 0:
            return
        
        # Check if mother killed
        # Chance for this on average is 10%, shouldn't I just change this to flat 10 or something?
        mother_cull = random.random() < self.settings.default_culling_rate().get_random_value()
        
        # Look for hot foxes in your area
        nearby_foxes = []

        # Track pregnant foxes separately (they stay in dens)
        mothers = []

        x_min = max(self.position.x-self.range, 0)
        x_max = min(self.position.x+self.range, self.population_manager.grid.shape[0]-1)
        y_min = max(self.position.y-self.range, 0)
        y_max = min(self.position.y+self.range, self.population_manager.grid.shape[1]-1)
        
        for fox in foxes:
            if x_min <= fox.current_position.x <= x_max and y_min <= fox.current_position.y <= y_max:
                if fox.is_pregnant:
                    mothers.append(fox)
                else:
                    nearby_foxes.append(fox)

        # Kill foxes
        killed_foxes = []

        # Kill mother first
        if mother_cull and len(mothers) > 0:
            killed_foxes.append(random.sample(mothers, 1)[0])
            foxes_killed -= 1

        # Kill the rest
        if foxes_killed > 0 and len(nearby_foxes) > 0:
            for fox in random.sample(nearby_foxes, min(foxes_killed, len(nearby_foxes))):
                killed_foxes.append(fox)

        # Remove killed foxes from the population
        for fox in killed_foxes:
            if fox.is_pregnant:
                print(f"Killed mother at {fox.current_position} from {fox.den_position}")
            else:
                print(f"Killed fox at {fox.current_position} from {fox.den_position}")
            self.population_manager.remove_fox(fox)

        # Move to a random position
        self.position = Vector2(random.choice(self.available_positions))

        # print(f"foxes I tried to kill: {foxes_killed}")
        # print(f"foxes I killed: {len(killed_foxes)}")
        # print(f"mothers I tried to kill: {1 if mother_cull else 0}")
        # print(f"mothers available: {len(mothers)}")
        # print(f"position: {self.position}")