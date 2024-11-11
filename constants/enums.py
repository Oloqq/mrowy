from enum import Enum


class TimeStep(int, Enum):
    HOURLY = 1
    EVERY_2_HOURS = 2
    EVERY_3_HOURS = 3
    DAY_PART = 4


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
    SOURCE = 2
    TARGET = 3
