import exifread
import glob
import datetime
import sys
from PIL import Image

# Open image file for reading (binary mode)
def getTags():
	imageTags = {}
	#get all images + names
	for f in glob.glob("*.jpg"):
		fileSchutff = open(f)
		tags = exifread.process_file(fileSchutff)
		#save time tag in {image:time}
		for tag in tags:
			imageTags[fileSchutff] = tags['EXIF DateTimeOriginal']
	# Return Exif tags
	return imageTags

def parseTags(tags):
	cleanTags = {}
	for fileWords,time in tags.items():
		#convert into Sting bc apparently they're not strings?
		fileString = str(fileWords)
		timeString = str(time)
		#turn strings into list
		#split by apostrophe
		imgName = fileString.split("'")[1]
		jankyTime = timeString.split()
		# third element in time is actual time
		timeClean = jankyTime[1]
		#remove seconds from cleanTime
		timeCleanWoSecond = timeClean[:5]
		cleanTags[timeCleanWoSecond] = imgName
	return cleanTags



#gets current time
def getCurrentTime():
	time = datetime.datetime.time(datetime.datetime.now())
	return time

#get current time not including seconds
def getCurrentTimewOSecond():
	time = datetime.datetime.time(datetime.datetime.now())
	strTime = str(time)
	return strTime[:5]

def main(args):
    print args

if __name__ == '__main__':
	main(sys.argv)
	tags = getTags()
	cleanTags = parseTags(tags)
	#current time
	# time = getCurrentTimewOSecond()
	# print merp,time
	time = '07:07'
	if time in cleanTags:
		image = Image.open(cleanTags[time])
		image.show()

	#print cleanTags

#print imageTags