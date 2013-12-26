#!/usr/bin/env python
import signal
import sys
import os
import subprocess
import logging
import pynotify
from pyudev import Context, Monitor, MonitorObserver

class DisplayManager:
    connected_displays = []

    def __init__(self):
        logging.debug('Initializing display manager')
        pynotify.init('AutoRandr')
        self.connected_displays = self.get_connected_displays()

    def device_event_listener(self, device):
        logging.debug('udev event {0.action}: {0.device_path}'.format(device))
        current_display_list = self.get_connected_displays()
        self.check_for_changes(current_display_list)
        
    def check_for_changes(self, current_display_list):
        for display in current_display_list:
            if display not in self.connected_displays:
                logging.debug('display connected: %s', display)
                self.connected_displays.append(display)
                self.send_notification('Display connected', display)
                self.displays_changed_listener()

        for display in self.connected_displays:
            if display not in current_display_list:
                logging.debug('display disconnected: %s', display)
                connected_displays.remove(display)
                self.send_notification('Display disconnected', display)
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

    def send_notification(self, title, message):
        notice = pynotify.Notification(title, message, os.path.abspath('img/video-display.png'))
        notice.show()