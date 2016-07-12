#!/usr/bin/python

# Import the SDK
import boto3
import botocore
import uuid
from progress_percentage import ProgressPercentage

BUCKET = 'scrum'


def getBucketName(s3):
        bucketList = getBucketList(s3)
	
	sbIndex = findBucketIndex(BUCKET, bucketList)
        
	if sbIndex > 0:
                print('Found: {0}'.format(sbIndex))
		return bucketList[sbIndex]
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
	 bucket.upload_file(filePath, storageKey)

def listKeysInBucket(bucket):
	for obj in bucket.objects.all():
		print(obj.key)

def main():
	
	print('Connecting to s3...')
        s3 = boto3.resource('s3')
	print('Getting the scrum bucket...')
        bucketName = getBucketName(s3)
	scrumBucket = s3.Bucket(bucketName)
	print('Listing the keys in our bucket...')
	listKeysInBucket(scrumBucket)
        print('Trying to upload our test file...')
	storeInBucket(scrumBucket, './test.txt', 'test.txt')
	
	print('Again listing the keys...')
	listKeysInBucket(scrumBucket)
	
	
		
if __name__ == "__main__":
    main()

