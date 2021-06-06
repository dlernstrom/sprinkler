"""This is the core app, when executed from the command line."""
import logging
import sys
import time

from __version__ import ROOT_DIR
from scheduler.scheduler_gallon import SchedulerGallon
from scheduler.scheduler_time import SchedulerTime

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


def run_app():
    """This is the core application method"""
    # scheduler = SchedulerGallon()
    scheduler = SchedulerTime()
    try:
        while scheduler.is_running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        scheduler.shutdown()
        raise


if __name__ == '__main__':
    try:
        run_app()
    except KeyboardInterrupt:
        pass
