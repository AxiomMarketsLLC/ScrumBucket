#!/usr/bin/python

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
from Tkinter import *


from watchdog.observers import Observer
from dir_event_handler import DirEventHandler
BUCKET = 'scrum'
PHOTO_DIR = '/home/pi/ScrumBucket/'
DEBUG = False
TEST_FILE = './test.txt'
TEST_KEY = 'test.txt'
CMD = './camera.sh'
CONNECT_CMD = 'c\n'
REC_MODE_CMD = 'rec\n'
REM_SHOOT_CMD = 'rs\n'
ERR_MSG = 'ERROR'
SUCCESS_MSG = 'SUCCESS'
ALREADY_REC_MSG = 'already in rec mode'
DELAY = 20 #interval in seconds for pics
KEY = "scrumImage"


def testBucketFunctions(bucket):
	print('Listing the keys in our bucket...')
        listKeysInBucket(bucket)
        print('Trying to upload our test file...')
        storeInBucket(bucket, TEST_FILE, TEST_KEY)
        print
        print('Again listing the keys...')
        listKeysInBucket(bucket)
        print('Removing test file...')
        removeFromBucket(bucket, TEST_KEY)
        print('Again listing the keys...')
        listKeysInBucket(bucket)


def getBucketName(s3):
        bucketList = getBucketList(s3)
	bucketIndex = findBucketIndex(BUCKET, bucketList)
        
	if bucketIndex > 0:
                print('Found: {0}'.format(bucketIndex))
		return bucketList[bucketIndex]
        else:
                print('Failed; could not find the scrum bucket!')
                return -1

def getBucketList(s3):
	bucketList = []
	for bucket in s3.buckets.all():
	    	bucketList.append(bucket.name)
	return bucketList;

def findBucketIndex(bucketName, bucketList):
	for i, s in enumerate(bucketList):
        	if bucketName in s:
              		return i
    	return -1

def storeInBucket(bucket, filePath, storageKey):
	 bucket.upload_file(filePath, storageKey, Callback=ProgressPercentage(filePath))

def listKeysInBucket(bucket):
	for obj in bucket.objects.all():
		print(obj.key)

def removeFromBucket(bucket,keyName):
        for obj in bucket.objects.all():
               if(obj.key == keyName):
                   response = bucket.delete_objects(Delete={'Objects': [{'Key': keyName}]})
                   return response
        return -1

def closeIfError(process, label):
	while(True):
		for line in iter(process.stderr.readline,''):
   	
			print("Camera err: " + line)
   			if(line.find(ERR_MSG) != -1 and line.find(ALREADY_REC_MSG)==-1):
				label['bg']='red'
				label['text']=ERR_MSG

def photoLoop(process, bucket, errThread, widget,tk, event_handler):
        time.sleep(1)
        process.stdin.write(CONNECT_CMD)
        time.sleep(1)
        process.stdin.write(REC_MODE_CMD)
        time.sleep(1)

	process.stdin.write(REM_SHOOT_CMD)
	time.sleep(5)
        key = KEY + " " + str(datetime.datetime.now())
        imagePath = event_handler.getImage()
        if(imagePath != -1):
		storeInBucket(bucket,imagePath,key)
		widget['text']= SUCCESS_MSG
		widget['bg']='green' 
	tk.after(DELAY*1000, lambda: threading.Thread(photoLoop(process,bucket,errThread,widget,tk,event_handler)).start())
def main():
	if DEBUG:
		logging.basicConfig(level=logging.DEBUG)
	
	print("Connecting to s3...")
        s3 = boto3.resource('s3')

	print('Getting the scrum bucket...')
        bucketName = getBucketName(s3)
	scrumBucket = s3.Bucket(bucketName)
        
	if DEBUG:
		testBucketFunctions(scrumBucket)

 	root = Tk()
	
	msg ="Wait for it"
	label = Label(root, text=msg, width=50, height=25, bg="grey")
        label.pack() 
	
        event_handler = DirEventHandler()
        observer = Observer()
        observer.schedule(event_handler,PHOTO_DIR,recursive=True)
        observer.start()
	
	cam = Popen([CMD],stdin=PIPE, stderr=PIPE)
	readCam = threading.Thread(target=closeIfError, args=(cam,label))
	readCam.start()
		
	root.after(2000, lambda: threading.Thread(photoLoop(cam,scrumBucket,readCam,label,root,event_handler)).start())

	root.mainloop()
if __name__ == "__main__":
    main()

