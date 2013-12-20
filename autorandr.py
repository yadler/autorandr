#!/usr/bin/env python
import signal
import sys
import subprocess
from pyudev import Context, Monitor, MonitorObserver

class UDevObserver:
    SUBSYSTEM_TO_MONITOR = 'drm'

    def __init__(self, udev_callback):
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem = self.SUBSYSTEM_TO_MONITOR)
        self.observer = MonitorObserver(monitor, callback = udev_callback, name = 'udev-observer')
        self.observer.daemon #= False

    def start(self):
        print 'starting observer...'
        self.observer.start()

    def stop(self):
        print 'stopping observer...'
        self.observer.stop()

class DisplayManager:
    INTERNAL_DISPLAYS = ['LVDS']
    EXTERNAL_DISPLAYS = ['DP', 'VGA']
    connected_displays = []

    def __init__(self):
        self.connected_displays = self.get_connected_displays()

    def device_event_listener(self, device):
        print('DM: background event {0.action}: {0.device_path}'.format(device))
        current_display_list = self.get_connected_displays()
        self.check_for_changes(current_display_list)

    def check_for_changes(self, current_display_list):
        for display in current_display_list:
            if display not in self.connected_displays:
                print 'new display connected: ' + display
                self.connected_displays.append(display)

        for display in self.connected_displays:
            if display not in current_display_list:
                print 'display got removed: ' + display
                self.connected_displays.remove(display)

    def get_connected_displays(self):
        process = subprocess.Popen("xrandr | grep ' connected' | cut -f1 -d' '", shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        errcode = process.returncode
        display_list = filter(None, out.split('\n'))
        return display_list


def signal_handler(signal, frame):
        print 'exiting!'
        observer.stop()
        sys.exit(0)

print 'autoRandr - press Ctrl+C to exit'
signal.signal(signal.SIGINT, signal_handler)

display_manager = DisplayManager()
observer = UDevObserver(display_manager.device_event_listener)
observer.start()

signal.pause()