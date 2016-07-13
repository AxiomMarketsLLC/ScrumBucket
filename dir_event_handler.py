
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time

from watchdog.events import FileSystemEventHandler


class DirEventHandler(FileSystemEventHandler):
	
	def __init__(self):
		super(DirEventHandler,self).__init__()
		self.hasImage=False
		self.lastPath=""

	def catch_all_handler(self, event):
        	logging.debug(event)
		print('Caught new file event')
		if (event.src_path.find('.jpg') != -1):
			print(event.src_path)
			self.hasImage=True
			self.lastPath=event.src_path
	def getImage(self):
		if self.hasImage:
			self.hasImage=False
			return self.lastPath
		else:
			return -1

	def on_moved(self, event):
    #    self.catch_all_handler(event)
		pass
	def on_created(self, event):
        	self.catch_all_handler(event)
	def on_deleted(self, event):
    #    self.catch_all_handler(event)
		pass
	def on_modified(self, event):
   #     self.catch_all_handler(event)
		pass
