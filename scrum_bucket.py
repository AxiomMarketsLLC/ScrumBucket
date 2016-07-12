#!/usr/bin/python

# Import the SDK
import boto3
import uuid

BUCKET = 'scrum'


def getBucketName(s3):

        print('Finding the scrum bucket....')
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

def main():
	
	print('Connecting to s3...')
        s3 = boto3.resource('s3')
        bucketName = getBucketName(s3)

        
	
	
		
if __name__ == "__main__":
    main()

