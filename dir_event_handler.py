#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time

from watchdog.events import FileSystemEventHandler


class DirEventHandler(FileSystemEventHandler):
    def catch_all_handler(self, event):
        logging.debug(event)
	print('Caught new file event')

    def on_moved(self, event):
        self.catch_all_handler(event)

    def on_created(self, event):
        self.catch_all_handler(event)

    def on_deleted(self, event):
        self.catch_all_handler(event)

    def on_modified(self, event):
        self.catch_all_handler(event)
