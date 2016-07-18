
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time

from watchdog.events import FileSystemEventHandler
import threading

class DirEventHandler(FileSystemEventHandler):
	
	def __init__(self, app):
		super(DirEventHandler,self).__init__()
		self.hasImage=False
		self.lastPath=""
		self.app=app

	def catch_all_handler(self, event):
        	logging.debug(event)
		print('Caught new file event')
		if (event.src_path.find('.jpg') != -1):
			print(event.src_path)
			threading.Thread(app.uploadImage(event.src_path)).start()
		

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
