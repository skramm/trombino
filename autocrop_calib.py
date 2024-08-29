#!/usr/bin/env python3

# GUI app, designed to manually find correct parameters for face detection

# 1 argument required: full filename

#----------------------------------------------
# Default Parameters, will be adjusted with trackbars
# see https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html
minBBsize=60
maxBBsize=120
scaleFactor=2.0
minNeighbors=5
#----------------------------------------------

# used to adapt large images to the screen
ViewScale=1.0

import os
import sys
import cv2
import pathlib
from pathlib import Path

window="calib"
font = cv2.FONT_HERSHEY_SIMPLEX

# predeclaration (needed coz used in trackbar callback)
img=None

'''
scaleFactor	Parameter specifying how much the image size is reduced at each image scale.
minNeighbors	Parameter specifying how many neighbors each candidate rectangle should have to retain it.
flags	Parameter with the same meaning for an old cascade as in the function cvHaarDetectObjects. It is not used for a new cascade.
minSize	Minimum possible object size. Objects smaller than that are ignored.
maxSize
'''

def processDetection():
	img = img_src
	print( "Detection: image size=", img.size, " shape=", img.shape )

	face_classifier = cv2.CascadeClassifier(
	    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
	)
	face = face_classifier.detectMultiScale(
		gray_image
		,scaleFactor=scaleFactor
		,minNeighbors=minNeighbors
		,minSize=(minBBsize, minBBsize)
#		,maxSize=(maxBBsize, maxBBsize)
	)
	if len(face) == 0:
		print( "Failed to find face!")
	else:
#		print( "nd rect=", face )
		print( "size=", face.size, " ndim=", face.ndim, " shape=", face.shape )
		print( " shape r=", face.shape[0], " shape c=", face.shape[1] )
		for (x, y, w, h) in face:
			cv2.putText( img, str(w)+"x"+str(h), (x,y), font, 1.0, (0,250,250) )
			cv2.rectangle(img, (x, y), (x + w, y + h), (128, 255, 0), 2)
			deltax=w/3
			deltay=h/2
			x0 = int( x - deltax   )
			y0 = int( y - deltay   )
			w0 = int( w + 2*deltax )
			h0 = int( h + 2*deltay )
			cv2.rectangle(img, (x0, y0), (x0 + w0, y0 + h0), (255, 255, 0), 2)


	cv2.imshow(window,img)


# scaleFactor
def on_trackbar_sf(val):
	scaleFactor = val / 10
	print( "scale factor=", scaleFactor )
	processDetection()
	if img != None: 
		cv2.imshow( window, img )

# minNeighbors
def on_trackbar_mn(val):
	minNeighbors = val
	print( "minNeighbors=", minNeighbors )
	processDetection()
	if img != None: 
		cv2.imshow( window, img )

# minSize
def on_trackbar_min(val):
	minBBsize = val
	print( "minBBsize=", minBBsize )
	processDetection()
	if img != None: 
		cv2.imshow( window, img )

# maxSize
def on_trackbar_max(val):
	maxBBsize = val
	print( "maxBBsize=", maxBBsize )
	processDetection()
	if img != None: 
		cv2.imshow( window, img )


#=====================================================================
# BEGIN

if( len(sys.argv) != 2 ):
	print( "Error, require 1 argument: filename" )
	exit(1)
	
fullfname = sys.argv[1]
#print( "fullfname=", fullfname )


img_src = cv2.imread(fullfname)
if img_src is None:
	print( "failed to read image, quitting..." )
	exit(2)
	
print( "input image size=", img_src.size, " size=", img_src.shape, "w=", img_src.shape[1]  )
gray_image = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

cv2.namedWindow(window)

cv2.createTrackbar( "Scale Factor",  window , int(scaleFactor*10), 30, on_trackbar_sf)
cv2.createTrackbar( "min Neighbors", window , minNeighbors,        20, on_trackbar_mn)
cv2.createTrackbar(  "min size",      window , minBBsize,           minBBsize*2, on_trackbar_min )
cv2.createTrackbar(  "max size",      window , maxBBsize,           int(img_src.shape[1]/2), on_trackbar_max )

#cv.createTrackbar("tb3", title_window , 0, max3, on_trackbar3)


while True:

	processDetection()

#	cv2.imshow(window,img)
	key=cv2.waitKey(0)
	if key == 27:
		break


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



