"""This is the core app, when executed from the command line.  Haven't decided whether I will leave this as a service
executable with an API or integrate it into a straight-up Django project
"""
import logging
import sys
import time

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

from __version__ import ROOT_DIR, APP_VERSION
from constants import GALLONS_PER_CLICK, GPIO_PIN, BOUNCE_TIME, NUMATO_IP, NUMATO_PASS, NUMATO_USER, \
    TURN_GALLONS_ALLOC, ZONES_USED
from numato import Numato

ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(logging.DEBUG)
ROOT_LOGGER.addHandler(logging.NullHandler())

SYS_CTL_LOG_FMT = '%(asctime)s %(name)-30s %(filename)-28s [%(lineno)-4d] %(levelname)-7s %(message)s'
SYSCTL_HANDLER = logging.StreamHandler(sys.stdout)
SYSCTL_HANDLER.setLevel(logging.DEBUG)
SYSCTL_HANDLER.setFormatter(logging.Formatter(SYS_CTL_LOG_FMT))
ROOT_LOGGER.addHandler(SYSCTL_HANDLER)

logger = logging.getLogger(__name__)
sys.path.insert(0, ROOT_DIR)


class Tracker:
    def __init__(self, gallons_allowed, zones_used):
        self.numato = Numato(NUMATO_IP, NUMATO_USER, NUMATO_PASS)
        self.numato.connect()
        self.start_time = time.perf_counter()
        self.gallons_used = 0
        self.gallons_allowed = gallons_allowed
        self.zones_used = zones_used
        self.zone_count = len(self.zones_used)
        self.current_zone = 0
        self.gallons_per_zone = gallons_allowed / self.zone_count

        self.numato.relay_on(self.zones_used[self.current_zone])

    def shutdown(self):
        self.numato.relay_off(self.zones_used[self.current_zone])
        self.numato.shutdown()

    def record_event(self):
        self.gallons_used += 10
        this_time = time.perf_counter()
        elapsed = this_time - self.start_time
        self.start_time = this_time
        gps = GALLONS_PER_CLICK / elapsed
        gpm = gps * 60
        gallons_remaining = self.gallons_allowed - self.gallons_used
        minutes_remaining = gallons_remaining / gpm
        hours_remaining = minutes_remaining // 60
        min_frac_remaining = minutes_remaining - hours_remaining * 60
        logger.debug(f"GPIO Water Meter Event! - %f gpm - elapsed time: %f, %02d:%02d remain",
                     gpm, elapsed, hours_remaining, min_frac_remaining)
        self.potentially_change_zones()

    def potentially_change_zones(self):
        current_zone_change_point = (self.current_zone + 1) * self.gallons_per_zone
        if self.gallons_used > current_zone_change_point:
            logger.warning('Changing Zones, moving from zone %d to zone %d', self.current_zone, self.current_zone + 1)
            logger.warning('%d gallons left', self.gallons_allowed - self.gallons_used)
            self.change_zones()

    def change_zones(self):
        self.numato.relay_off(self.zones_used[self.current_zone])
        self.current_zone += 1
        self.numato.relay_on(self.zones_used[self.current_zone])


tracker = Tracker(TURN_GALLONS_ALLOC, ZONES_USED)


def gpio_callback(channel):
    global tracker
    if not GPIO.input(GPIO_PIN):
        return
    logger.warning('Event Detected')
    tracker.record_event()


def setup_gpio():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # Setup event on pin 10 trigger on both rising and falling
    GPIO.add_event_detect(GPIO_PIN, GPIO.BOTH, callback=gpio_callback, bouncetime=BOUNCE_TIME)


def run_app():
    """This is the core application method"""
    setup_gpio()
    try:
        logger.warning('We get to water for %d gallons this turn', TURN_GALLONS_ALLOC)
        while tracker.current_zone < tracker.zone_count:
            time.sleep(0.5)
    except KeyboardInterrupt:
        tracker.shutdown()
        raise
    finally:
        GPIO.cleanup()  # Clean up


if __name__ == '__main__':
    try:
        run_app()
    except KeyboardInterrupt:
        pass
