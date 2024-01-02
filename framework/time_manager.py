from settings.time_manager_settings import get_default_time_manager_settings, TimeManagerSettings
from constants.enums import DayPart, TimeStep
from astral import Astral
from typing import Any
import numpy as np
import datetime


class DayCycle:

    def __init__(self, city: Any, date: datetime.datetime):
        self.city = city
        self.date = date
        self.sun = self.city.sun(date=date, local=True)
        self.sunrise = self.sun['sunrise']
        self.sunset = self.sun['sunset']
        self.times_of_day = self.get_times_of_day()

    def get_times_of_day(self):
        hours = np.full(24, DayPart.NIGHT, dtype=DayPart)
        hours[self.sunrise.hour:self.sunset.hour] = DayPart.DAY
        hours[self.sunrise.hour - 1] = DayPart.DAWN
        hours[self.sunset.hour] = DayPart.DUSK

        return hours

    def __getitem__(self, item):
        return self.times_of_day[item]


class TimeManager:
    settings: TimeManagerSettings
    current_day_cycle: DayCycle
    date: datetime.datetime
    time_step: TimeStep

    def __init__(self, time_step: TimeStep):
        self.settings = get_default_time_manager_settings()
        self.astral_client = Astral()
        self.city = self.astral_client[self.settings.CITY_NAME]
        self.date = datetime.datetime(self.settings.INITIAL_YEAR, self.settings.INITIAL_MONTH,
                                      self.settings.INITIAL_DAY, 0, 0, 0)
        self.current_day_cycle = self.create_day_cycle()
        self.time_step = time_step

    def create_day_cycle(self):
        return DayCycle(self.city, self.date)

    def perform_time_step(self):
        if self.time_step == TimeStep.HOURLY:
            # Check if we passed onto the next day
            self.date = self.date + datetime.timedelta(hours=1)

            if self.date.day != self.current_day_cycle.date.day:
                self.current_day_cycle = self.create_day_cycle()

            current_hour = self.date.hour
            return self.current_day_cycle[current_hour]



