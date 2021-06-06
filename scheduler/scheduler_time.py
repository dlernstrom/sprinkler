import logging
import time

from constants import ZONES_USED, WATERING_TIME_HOURS
from scheduler.scheduler_base import SchedulerBase

logger = logging.getLogger(__name__)


class SchedulerTime(SchedulerBase):
    def __init__(self):
        super().__init__()
        self.seconds_per_zone = 3600.0 * WATERING_TIME_HOURS / self.zone_count
        logger.warning('We get to water for %d hours', WATERING_TIME_HOURS)
        logger.warning('Will change zones after %d minutes', self.seconds_per_zone // 60)

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
        """Returns in float minutes"""
        return (time.perf_counter() - self.start_time) / 60.0

    def change_zones(self):
        super().change_zones()
        logger.warning('%d minutes left', int(60.0 * WATERING_TIME_HOURS - self.total_elapsed_time))
