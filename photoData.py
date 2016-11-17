import exifread
import glob
import datetime

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
		allWordsInTag = fileString.split()
		jankyTime = timeString.split()
		# take third word which is the image name
		idimgName = allWordsInTag[2]
		# third element in time is actual time
		timeClean = jankyTime[1]
		cleanTags[idimgName] = timeClean
	return cleanTags



#gets current time
def getCurrentTime():
	time = datetime.datetime.time(datetime.datetime.now())
	return time

tags = getTags()
cleanTags = parseTags(tags)
print cleanTags


#print imageTags