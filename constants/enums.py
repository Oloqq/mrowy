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


class FieldType(Enum):
    GRASS = 0
    FOREST = 1
    WATER = 2
    URBAN = 3
    PATH = 4
    BUILDINGS = 5


class ObjectType(Enum):
    NOTHING = 0
    HUNTER = 1
    FOX_DEN = 2
    RABBIT_DEN = 3


class DayPart(Enum):
    NIGHT = 0
    DAY = 1
    DAWN = 2
    DUSK = 3
