#!/usr/bin/env python

# libs
import signal
import sys
import subprocess
import logging
from pyudev import Context, Monitor, MonitorObserver

# submodules
from display_manager import DisplayManager
from udev_observer import UDevObserver

class AutoRandr:
    def __init__(self):
        print 'autoRandr - press Ctrl+C to exit\n'
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
        logging.info('Starting AutoRandr')

        display_manager = DisplayManager()
        self.observer = UDevObserver(display_manager.device_event_listener)
        self.observer.start()

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()

    def signal_handler(self, signal, frame):
            print 'exiting!'
            self.observer.stop()
            sys.exit(0)

if __name__ == '__main__':
    AutoRandr()


    ## todo: make autorandr a possible solution for
    # http://askubuntu.com/questions/73804/wrong-login-screen-resolution