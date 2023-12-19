from dataclasses import dataclass


@dataclass
class TimeManagerSettings:
    INITIAL_YEAR: int = 2020
    INITIAL_MONTH: int = 1
    INITIAL_DAY: int = 1
    CITY_NAME: str = 'Warsaw'


def get_default_time_manager_settings() -> TimeManagerSettings:
    return TimeManagerSettings()
