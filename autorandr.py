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

class DisplayManager:
    INTERNAL_DISPLAYS = ['LVDS']
    EXTERNAL_DISPLAYS = ['DP', 'VGA']
    connected_displays = []

    def __init__(self):
        logging.debug('Initializing display manager')
        self.connected_displays = self.get_connected_displays()

    def device_event_listener(self, device):
        logging.debug('udev event {0.action}: {0.device_path}'.format(device))
        current_display_list = self.get_connected_displays()
        self.check_for_changes(current_display_list)

    def check_for_changes(self, current_display_list):
        for display in current_display_list:
            if display not in self.connected_displays:
                logging.debug('new display connected: %s', display)
                self.connected_displays.append(display)
                self.displays_changed_listener()

        for display in self.connected_displays:
            if display not in current_display_list:
                logging.debug('display got removed: %s', display)
                connected_displays.remove(display)
                self.displays_changed_listener()

        logging.debug('current display_list: %s', ', '.join(self.connected_displays))

    def displays_changed_listener(self):
        logging.debug('displays changed - new profile: %s', self.get_current_profile())

    def get_current_profile(self):
        return "-".join(sorted(self.connected_displays))

    def get_connected_displays(self):
        process = subprocess.Popen("xrandr | grep ' connected' | cut -f1 -d' '", shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        errcode = process.returncode
        display_list = filter(None, out.split('\n'))
        return display_list

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