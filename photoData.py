import exifread
import glob
import datetime

# Open image file for reading (binary mode)
def getTags():
	imageTags = {}
	#get all images + names
	for f in glob.glob("*.jpg"):
		fileSchutff = open(f,'rb')
		tags = exifread.process_file(fileSchutff)
		#save time tag in {image:time}
		for tag in tags:
			imageTags[fileSchutff] = tags['EXIF DateTimeOriginal']
	# Return Exif tags
	return imageTags

def parseTags():
	

#gets current time
def getCurrentTime():
	time = datetime.datetime.time(datetime.datetime.now())
	return time



#print imageTags