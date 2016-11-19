import exifread
import glob
import datetime
import sys
import time
from PIL import Image

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

def showPhoto(dateRelevance):
	#if photo should be specific to date and time
	tags = getTags()
	if dateRelevance == True:
		cleanTags = parseTagsDateTime(tags)
		dateTime = getCurrentDateandTime()
		#if the data and time match, exclude the year
		if dateTime in cleanTags:
			image = Image.open(cleanTags[dateTime])
			image.show()
		else:
			pass

	else:
		cleanTags = parseTagsTime(tags)
		#current time
		time = getCurrentTimewOSecond()
		#for testing
		if time in cleanTags:
			image = Image.open(cleanTags[time])
			image.show()
		else:
			pass


def main(args):
    print args

if __name__ == '__main__':

	main(sys.argv)
	#run every 60 seconds
	while True:
		showPhoto(dateRelevance)
		timE = getCurrentTimewOSecond()
		print timE
		time.sleep(60)
	#print cleanTags

#print imageTags