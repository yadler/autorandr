#!/usr/bin/env python
import signal
import sys
import subprocess
import logging
from pyudev import Context, Monitor, MonitorObserver

class UDevObserver:
    SUBSYSTEM_TO_MONITOR = 'usb'

    def __init__(self, udev_callback):
        logging.debug('Initializing udev observer')
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem = self.SUBSYSTEM_TO_MONITOR)
        self.observer = MonitorObserver(monitor, callback = udev_callback, name = 'udev-observer')
        self.observer.daemon #= False

    def start(self):
        logging.info('Starting udev observer')
        self.observer.start()

    def stop(self):
        logging.info('Stopping udev observer')
        self.observer.stop()

