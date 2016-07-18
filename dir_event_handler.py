
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time
import datetime
from watchdog.events import FileSystemEventHandler
import threading
#Macros for key names
LATEST_NAME = 'latest'
EXTENSION = '.jpg'
KEY = "scrumImage"


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
			threading.Thread(self.uploadImage(event)).start()
	def uploadImage(self, event):
		key = (KEY + " " + str(datetime.datetime.now()) + EXTENSION).replace(" ","")
                self.app.storeInBucket(event.src_path,key)
                self.app.copyKeyInBucket(key, LATEST_NAME+EXTENSION)
                self.app.uiLock.acquire()
                self.app.label['text']= 'SUCCESS'
                self.app.label['bg']='green'
                self.app.root['bg']='green'
                self.app.uiLock.release()
		

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
