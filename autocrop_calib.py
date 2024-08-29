#!/usr/bin/env python3

# GUI app, designed to select parameters for face detection

# src: https://www.datacamp.com/tutorial/face-detection-python-opencv

# 1 argument required: full filename

#----------------------------------------------
# PARAMETERS (adjust if needed)
# see https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html
minBBsize=60
scaleFactor=2.0
#----------------------------------------------


import os
import sys
import cv2
import pathlib
from pathlib import Path

window="calib"
'''
scaleFactor	Parameter specifying how much the image size is reduced at each image scale.
minNeighbors	Parameter specifying how many neighbors each candidate rectangle should have to retain it.
flags	Parameter with the same meaning for an old cascade as in the function cvHaarDetectObjects. It is not used for a new cascade.
minSize	Minimum possible object size. Objects smaller than that are ignored.
maxSize
'''

def processDetection():
	face_classifier = cv2.CascadeClassifier(
	    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
	)
	face = face_classifier.detectMultiScale(
    	gray_image, scaleFactor=scaleFactor, minNeighbors=5, minSize=(minBBsize, minBBsize)
	)
	if len(face) == 0:
		print( "Failed to find face!")
	else:
		print( "nd rect=", face )
		print( "size=", face.size, " ndim=", face.ndim, " shape=", face.shape )
		print( " shape r=", face.shape[0], " shape c=", face.shape[1] )

		for (x, y, w, h) in face:
		    cv2.rectangle(img, (x, y), (x + w, y + h), (128, 255, 0), 4)

	cv2.imshow('window',img)


# scaleFactor
def on_trackbar_sf(val):
    scaleFactor = val / 10
	processDetection()
    cv.imshow(title_window, img)

# minNeighbors


if( len(sys.argv) != 2 ):
	print( "Error, require 1 argument: filename" )
	exit(1)
	
fullfname = sys.argv[1]
print( "fullfname=", fullfname )


img = cv2.imread(fullfname)
if img is None:
	print( "failed to read image, quitting..." )
	exit(2)
	
print( "input image size=", img.size, " size=", img.shape )
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv.namedWindow(window)
cv.createTrackbar("Scale Factor", window , 0, 20, on_trackbar_sf)
#cv.createTrackbar("tb2", title_window , 0, max2, on_trackbar2)
#cv.createTrackbar("tb3", title_window , 0, max3, on_trackbar3)


while True:
	processDetection()

	cv2.imshow(window,img)
	cv2.waitKey(0)


'''	
#print( "type of face=", type(face) )

if len(face) == 0:
	print( "Failed to find face, output file identical to input!" )
	cv2.imwrite(dir_out+"/"+fname,img)
	exit(0)

#print( "nd rect=", face )
print( "size=", face.size, " ndim=", face.ndim, " shape=", face.shape )
print( " shape r=", face.shape[0], " shape c=", face.shape[1] )

if( face.shape[0] != 1 ):
	print( "Failure, found ", face.shape[0], " faces in file ", sys.argv[1] )
	exit(4)

#for (x, y, w, h) in face:
#    cv2.rectangle(img, (x, y), (x + w, y + h), (128, 255, 0), 4)

deltax=face[0][2]/3
deltay=face[0][2]/2
x0 = int( face[0][0] - deltax   )
y0 = int( face[0][1] - deltay   )
w0 = int( face[0][2] + 2*deltax )
h0 = int( face[0][3] + 2*deltay )


#cv2.rectangle(img, (x0, y0), (x0 + w0, y0 + h0), (0, 255, 0), 4)

img_out = gray_image[y0:y0+h0,x0:x0+w0]
cv2.imwrite(dir_out+"/"+fname,img_out)
'''



