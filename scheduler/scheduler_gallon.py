import logging
import time

from pubsub import pub

from constants import GALLONS_PER_CLICK, TURN_GALLONS_ALLOC, ZONES_USED
from numato import Numato
from utils.ui_utils import min_to_time_str
from water_meter import WaterMeter

logger = logging.getLogger(__name__)


class SchedulerGallon:
    def __init__(self):
        self.meter = WaterMeter()
        self.numato = Numato()
        self.start_time = time.perf_counter()
        self.gallons_used = 0
        self.zone_count = len(ZONES_USED)
        self.current_zone = 0
        self.gallons_per_zone = TURN_GALLONS_ALLOC / self.zone_count

        self.numato.relay_on(ZONES_USED[self.current_zone])
        logger.warning('We get to water for %d gallons this turn', TURN_GALLONS_ALLOC)
        pub.subscribe(self.record_event, 'meter_event')

    def shutdown(self):
        self.numato.relay_off(ZONES_USED[self.current_zone])
        self.numato.shutdown()
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
        """Change zones to the next in the list"""
        old_zone_index = self.current_zone
        new_zone_index = self.current_zone + 1
        logger.warning('Changing Zones, moving from zone %d to zone %d', old_zone_index, new_zone_index)
        logger.warning('%d gallons left', TURN_GALLONS_ALLOC - self.gallons_used)
        self.current_zone += 1
        self.numato.relay_on(ZONES_USED[new_zone_index])
        self.numato.relay_off(ZONES_USED[old_zone_index])
