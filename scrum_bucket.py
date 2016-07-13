#!/usr/bin/python

# Import the SDK
import boto3
import botocore
import uuid
import time
import datetime
import logging
import threading
from subprocess32 import Popen, PIPE, STDOUT

from progress_percentage import ProgressPercentage
from watchdog.observers import Observer
from dir_event_handler import DirEventHandler

import sys

BUCKET = 'scrum'
PHOTO_DIR = '/home/pi/ScrumBucket/'
DEBUG = True
TEST_FILE = './test.txt'
TEST_KEY = 'test.txt'
CMD = './camera.sh'
CONNECT_CMD = 'c\n'
REC_MODE_CMD = 'rec\n'
REM_SHOOT_CMD = 'rs\n'
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

def closeIfError(process):
	
	for line in iter(process.stdout.readline,''):
   	
		print("Camera out: " + line)
   		if(line.find("ERROR") != -1):
			print("ERROR!")
			#process.stdin.close()
			#sys.exit(-1)

def main():
	if DEBUG:
		logging.basicConfig(level=logging.DEBUG)

	print('Connecting to s3...')
        s3 = boto3.resource('s3')

	print('Getting the scrum bucket...')
        bucketName = getBucketName(s3)
	scrumBucket = s3.Bucket(bucketName)
        
	if DEBUG:
		testBucketFunctions(scrumBucket)

 	
        event_handler = DirEventHandler()
        observer = Observer()
        observer.schedule(event_handler,PHOTO_DIR,recursive=True)
        observer.start()
	
	cam = Popen([CMD],stdin=PIPE,stdout=PIPE)
	readCam = threading.Thread(target=closeIfError, args=(cam,))
	readCam.start()
	
	time.sleep(1)
	cam.stdin.write(CONNECT_CMD)
	time.sleep(1)
	cam.stdin.write(REC_MODE_CMD)
	time.sleep(1)
	
	try:
		while True:
			cam.stdin.write(REM_SHOOT_CMD)
			time.sleep(DELAY/2)
    			key = KEY + " " + str(datetime.datetime.now())	
			imagePath = event_handler.getImage()
			if(imagePath != -1):
				threading.Thread(storeInBucket(scrumBucket, imagePath, key)).start()
			time.sleep(DELAY/2)
	except:
		print("Ending...")
		cam.stdin.close()
		
		
if __name__ == "__main__":
    main()

