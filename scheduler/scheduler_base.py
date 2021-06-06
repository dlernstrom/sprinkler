import logging
import time

from constants import ZONES_USED, SIMULTANEOUS_ZONES
from numato import Numato

logger = logging.getLogger(__name__)


class SchedulerBase:
    def __init__(self):
        self.zone_count = len(ZONES_USED)
        self.current_zone = None
        self.indexes_used = set()

        self.start_time = time.perf_counter()
        self.zone_start = self.start_time
        self.numato = Numato()
        self.change_zones()
        self.change_zones()

    def shutdown(self):
        logger.warning('Disconnecting from Numato.  In the future, we need to shut off pump, then zones')
        self.numato.shutdown()

    def change_zones(self):
        """Change zones to the next in the list"""
        old_zone_indexes = self.indexes_used
        old_zone_index = self.current_zone
        if self.current_zone is None:  # first time through
            self.current_zone = -1
        new_zone_index = self.current_zone + 1
        logger.warning('Changing Zones, moving from zone %s to zone %d', old_zone_index, new_zone_index)
        new_zone_indexes = set()
        for simultaneous_zone in range(SIMULTANEOUS_ZONES):
            new_index = new_zone_index + simultaneous_zone
            if new_index >= self.zone_count:
                new_index -= self.zone_count
            new_zone_indexes.add(new_index)
        self.current_zone += 1
        zones_to_turn_off = list(old_zone_indexes.difference(new_zone_indexes))
        zones_to_turn_on = list(new_zone_indexes.difference(old_zone_indexes))
        for zone_index in zones_to_turn_on:
            self.numato.relay_on(ZONES_USED[zone_index])
        for zone_index in zones_to_turn_off:
            self.numato.relay_off(ZONES_USED[zone_index])
        self.indexes_used = new_zone_indexes
        self.zone_start = time.perf_counter()
