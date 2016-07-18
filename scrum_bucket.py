#!/usr/bin/env python
# Import the SDK
import boto3
import botocore
import uuid
from progress_percentage import ProgressPercentage
import time
import datetime
import logging
import threading
from subprocess32 import Popen, PIPE, STDOUT
import sys
import socket
import fcntl
import struct
from Tkinter import *
import tkFont


from watchdog.observers import Observer
from dir_event_handler import DirEventHandler

PHOTO_DIR = '/home/pi/ScrumBucket/'
DEBUG = False
TEST_FILE = '/home/pi/test.txt'
TEST_KEY = 'test.txt'
CMD = PHOTO_DIR+'camera.sh'

#These are commands for the command line utility controlling the camera
CONNECT_CMD = 'c\n' #connect
REC_MODE_CMD = 'rec\n'#record mode
REM_SHOOT_CMD = 'rs\n'#remote shoot

ERR_MSG = 'ERROR'
SUCCESS_MSG = 'SUCCESS'
ALREADY_REC_MSG='already in rec'

INTERFACE = 'eth0' #change to wlan0 for wifi operation
VERSION = '0.1.0'

#Options for UI interval widget
TIME_OPTIONS = {"20 secs":20,"1 min":60,"15 mins":900, "30 mins":1800,"1 hour":3600}


#credit: http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
def getIP(interface):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', interface[:15])
    )[20:24])

class PhotoApp():

	def __init__(self, storeBucket, debug=DEBUG):
	
		self.uiLock = threading.Lock()
		self.debug = debug
	
		if debug:
                	logging.basicConfig(level=logging.DEBUG)
	
		self.storeBucket = storeBucket
        
		print("PHOTOAPP: Connecting to s3...")
	        self.s3 = boto3.resource('s3')

        	print('PHOTOAPP: Getting the scrum bucket...')
	        bucketName = self.getBucketName()
        	self.scrumBucket = self.s3.Bucket(bucketName)

	        if debug:
        	        self.testBucketFunctions()

	        self.root = Tk()
        	self.root.minsize(width=320, height=240)
	        self.root.maxsize(width=320, height=240)
        	msg ="Wait for it"

	        self.label = Label(self.root, text=msg,width=10, height=5)
        	self.label.pack(side=TOP)
	        iplabel = Label(self.root, text='IP: '+getIP(INTERFACE))
        	iplabel.pack(side=TOP)
	        vers_label = Label(self.root, text='VERSION: '+VERSION)
        	vers_label.pack(side=TOP)

                takePicButton = Button(self.root, text="SHOOT", command=self.snapPicture)
                takePicButton.pack(side=TOP)

	        self.interval = Spinbox(self.root,values=TIME_OPTIONS.keys(),wrap = True, font = tkFont.Font(size=18))
        	self.interval.pack()
	        self.event_handler = DirEventHandler(self)
        	observer = Observer()
	        observer.schedule(self.event_handler,PHOTO_DIR,recursive=True)
	        observer.start()

        	self.cam = Popen([CMD],stdin=PIPE, stderr=PIPE)
	        self.errorThread = threading.Thread(target=self.checkForError)
        	self.errorThread.start()

		self.root.after(1, lambda: threading.Thread(self.photoLoop()).start())
		self.root.mainloop()
	

	def testBucketFunctions(self):
		print('Listing the keys in our bucket...')
        	listKeysInBucket()
        	print('Trying to upload our test file...')
        	storeInBucket(TEST_FILE, TEST_KEY)
	        print
        	print('Again listing the keys...')
        	listKeysInBucket(self.scrumBucket)
	        print('Removing test file...')
        	removeFromBucket(self.scrumBucket, TEST_KEY)
        	print('Again listing the keys...')
	        listKeysInBucket(self.scrumBucket)

	def getBucketName(self):
        	bucketList = self.getBucketList()
		bucketIndex = self.findBucketIndex(bucketList)
        
		if bucketIndex > 0:
                	print('Found: {0}'.format(bucketIndex))
			return bucketList[bucketIndex]
        	else:
                	print('PHOTOAPP: Failed; could not find the scrum bucket!')
                	return -1
	def getBucketList(self):
		bucketList = []
		for bucket in self.s3.buckets.all():
	    		bucketList.append(bucket.name)
		return bucketList;
	def findBucketIndex(self, bucketList):
		for i, s in enumerate(bucketList):
        		if self.storeBucket in s:
              			return i
    		return -1
	def storeInBucket(self, filePath, storageKey):
		 return self.scrumBucket.upload_file(filePath, storageKey, Callback=ProgressPercentage(filePath))
	def listKeysInBucket(self):
		for obj in scrumBucket.objects.all():
			print(obj.key)
	def copyKeyInBucket(self, fromName, toName):
		return self.s3.Object(self.scrumBucket.name, toName).copy_from(CopySource=self.scrumBucket.name+'/'+fromName)
	def removeFromBucket(self,keyName):
		for obj in self.scrumBucket.objects.all():
			if(obj.key == keyName):
                   		response = self.scrumBucket.delete_objects(Delete={'Objects': [{'Key': keyName}]})
                   		return response
	        return -1
	def checkForError(self):
		while(True):
			for line in iter(self.cam.stderr.readline,''):
				print("Camera err: " + line)
   				if(line.find(ERR_MSG) != -1 and line.find(ALREADY_REC_MSG)==-1):
					self.uiLock.acquire()
					self.root['bg']='red'
					self.label['bg']='red'
					self.label['text']=ERR_MSG
					self.uiLock.release()
	def getInterval(self):
		delay = TIME_OPTIONS[self.interval.get()]
		return delay
	
	def snapPicture(self):
	        self.cam.stdin.write(CONNECT_CMD)
                time.sleep(1)
                self.cam.stdin.write(REC_MODE_CMD)
                time.sleep(1)
                self.cam.stdin.write(REM_SHOOT_CMD)

	def photoLoop(self):
        	self.snapPicture()      

		if self.debug:
				self.listKeysInBucket()
		self.root.after(self.getInterval()*1000, lambda: threading.Thread(self.photoLoop()).start())
if __name__ == "__main__":
	photoApp = PhotoApp('scrum')

