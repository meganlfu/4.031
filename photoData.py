import exifread
import glob
import datetime
import sys
import time
from PIL import Image
import cv2
import numpy as np

dateRelevance = False

# Open image file for reading (binary mode)
def getTags():
	imageTags = {}
	#get all images + names
	for f in glob.glob("photos/*.jpg"):
		fileSchutff = open(f)
		tags = exifread.process_file(fileSchutff)
		#save time tag in {image:time}
		for tag in tags:
			imageTags[fileSchutff] = tags['EXIF DateTimeOriginal']
		#to subvert to many files open error for python
		fileSchutff.close()
	# Return Exif tags
	return imageTags

def parseTagsTime(tags):
	'''takes in a dictionary of EXIF tags and returns a dictionary of {(date,time):image name}'''
	cleanTags = {}
	for fileWords,time in tags.items():
		#convert into Sting bc apparently they're not strings?
		fileString = str(fileWords)
		timeString = str(time)
		#turn strings into list
		#split by apostrophe
		imgName = fileString.split("'")[1]
		jankyTime = timeString.split()
		# second element in time is actual time
		timeClean = jankyTime[1]
		#remove seconds from cleanTime
		timeCleanWoSecond = timeClean[:5]
		cleanTags[timeCleanWoSecond] = imgName
	return cleanTags

def parseTagsDateTime(tags):
	'''takes in a dictionary of EXIF tags and returns a dictionary of {date,time:image name} w/o year or second'''
	cleanTags = {}
	for fileWords,dateTime in tags.items():
		#convert into Sting bc apparently they're not strings?
		fileString = str(fileWords)
		timeString = str(dateTime)
		#turn strings into list
		#split by apostrophe
		imgName = fileString.split("'")[1]
		jankyDateTime = timeString.split()
		jankyDate = jankyDateTime[0]
		jankyTime = jankyDateTime[1]

		date = jankyDate[5:]
		time = jankyTime[:5]
		# third element in time is actual time
		# timeClean = jankyTime[1]
		#remove seconds from cleanTime
		# timeCleanWoSecond = timeClean[:5]
		cleanTags[(date,time)] = imgName
	return cleanTags

#gets current time
def getCurrentTime():
	'''returns current time, seconds included'''
	time = datetime.datetime.time(datetime.datetime.now())
	return time

#get current time not including seconds
def getCurrentTimewOSecond():
	'''returns current time exluding the seconds'''
	time = datetime.datetime.time(datetime.datetime.now())
	strTime = str(time)
	return strTime[:5]

def getCurrentDateandTime():
	'''returns a tuple with the date (not including year) and time'''
	time = getCurrentTimewOSecond()
	dateTime = datetime.datetime.now()
	justDate = dateTime.strftime("%m-%d")
	betterDate = justDate.replace ("-", ":")
	return (betterDate,time)

def getPhoto(dateRelevance,tags):
	'''returns the name of the photo, or None if no photo matches the tag'''
	#if photo should be specific to date and time
	if dateRelevance == True:
		cleanTags = parseTagsDateTime(tags)
		dateTime = getCurrentDateandTime()
		#if the data and time match, exclude the year
		if dateTime in cleanTags:
			return cleanTags[dateTime]
		else:
			return None
	#just show photo based on time, not on date as well
	else:
		cleanTags = parseTagsTime(tags)
		#current time
		currentTime = getCurrentTimewOSecond()
		#testing
		#currentTime = "04:04"
		if currentTime in cleanTags:
			return cleanTags[currentTime]
		else:
			return None

def showPhoto(path):
	'''displays the image and then closes it afte 60 seconds'''
	img = cv2.imread(path)
	#create a standard window for everything to be shown through
	cv2.namedWindow('fu',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('fu', 600,600)
	cv2.imshow('fu', img)
	#keeps the image open for 60 seconds
	cv2.waitKey(1)
	time.sleep(60)

def displayCameraFeed():
	cameraPort = 0
	testFrames = 30
	camera = cv2.VideoCapture(cameraPort)

def main(args):
    print args

if __name__ == '__main__':

	main(sys.argv)
	#run every 60 seconds
	while True:
		tags = getTags()
		currentTime = getCurrentTimewOSecond()
		print currentTime
		currentPhoto = getPhoto(dateRelevance,tags)
		if currentPhoto != None:
			showPhoto(currentPhoto)
		else:
			print "no photo, use camera"
			time.sleep(60)
	#print cleanTags

#print imageTags