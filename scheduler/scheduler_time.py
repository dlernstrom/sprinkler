import logging
import time

from constants import ZONES_USED, WATERING_TIME_HOURS
from numato import Numato

logger = logging.getLogger(__name__)


class SchedulerTime:
    def __init__(self):
        self.numato = Numato()
        self.start_time = time.perf_counter()
        self.zone_start = self.start_time
        self.zone_count = len(ZONES_USED)
        self.current_zone = 0

        self.seconds_per_zone = 360.0 * WATERING_TIME_HOURS / self.zone_count
        self.numato.relay_on(ZONES_USED[self.current_zone])
        logger.warning('We get to water for %d hours', WATERING_TIME_HOURS)

    def shutdown(self):
        self.numato.relay_off(ZONES_USED[self.current_zone])
        self.numato.shutdown()

    @property
    def is_running(self):
        if time.perf_counter() < self.zone_start + self.seconds_per_zone:
            return True
        if time.perf_counter() > self.start_time + self.zone_count * self.seconds_per_zone:
            return False
        self.change_zones()
        return True

    @property
    def total_elapsed_time(self):
        return (time.perf_counter() - self.start_time) / 60.0

    def change_zones(self):
        """Change zones to the next in the list"""
        old_zone_index = self.current_zone
        new_zone_index = self.current_zone + 1
        logger.warning('Changing Zones, moving from zone %d to zone %d', old_zone_index, new_zone_index)
        logger.warning('%d minutes left', 60.0 * WATERING_TIME_HOURS - self.total_elapsed_time)
        self.current_zone += 1
        self.numato.relay_on(ZONES_USED[new_zone_index])
        self.numato.relay_off(ZONES_USED[old_zone_index])
