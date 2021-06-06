import logging
import time

from pubsub import pub

from constants import GALLONS_PER_CLICK, TURN_GALLONS_ALLOC
from scheduler.scheduler_base import SchedulerBase
from utils.ui_utils import min_to_time_str
from water_meter import WaterMeter

logger = logging.getLogger(__name__)


class SchedulerGallon(SchedulerBase):
    def __init__(self):
        self.meter = WaterMeter()
        self.gallons_used = 0
        self.gallons_per_zone = TURN_GALLONS_ALLOC / self.zone_count
        super().__init__()

        logger.warning('We get to water for %d gallons this turn', TURN_GALLONS_ALLOC)
        pub.subscribe(self.record_event, 'meter_event')

    def shutdown(self):
        super().shutdown()
        pub.unsubscribe(self.record_event, 'meter_event')

    @property
    def is_running(self):
        return self.current_zone < self.zone_count

    def record_event(self):
        self.gallons_used += 10
        this_time = time.perf_counter()
        elapsed = this_time - self.start_time
        self.start_time = this_time
        gps = GALLONS_PER_CLICK / elapsed
        gpm = gps * 60
        logger.debug(
            "GPIO Water Meter Event! - %f gpm, %s zone remain, %s total remain",
            gpm, min_to_time_str(self.zone_gallons_remaining / gpm), min_to_time_str(self.total_gallons_remaining / gpm)
        )
        if self.zone_gallons_remaining == 0 and self.total_gallons_remaining > 0:
            self.change_zones()
        elif self.total_gallons_remaining == 0:
            logger.warning('Watering completed.  Total Gallons Remaining at Zero')

    @property
    def total_gallons_remaining(self):
        return max(TURN_GALLONS_ALLOC - self.gallons_used, 0)

    @property
    def zone_gallons_remaining(self):
        current_zone_change_point = (self.current_zone + 1) * self.gallons_per_zone
        return max(current_zone_change_point - self.gallons_used, 0)

    def change_zones(self):
        super().change_zones()
        logger.warning('%d gallons left', TURN_GALLONS_ALLOC - self.gallons_used)
