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
viewScale=1.0

import os
import sys
import cv2
import pathlib
from pathlib import Path

window="calib"
font = cv2.FONT_HERSHEY_SIMPLEX
iterIdx=0
# predeclaration (needed coz used in trackbar callback)
img=None
img2=None


#=====================================================================
# main detection function
def processDetection():
	global iterIdx,img2
	iterIdx=iterIdx+1

	img = img_src.copy()
#	print("viewScale=", viewScale)
	img2 = cv2.resize(img,  (int(img.shape[1]/viewScale), int(img.shape[0]/viewScale )))
# this does not work, but it should! (?)
# see https://docs.opencv.org/4.6.0/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d
#	img2 = cv2.resize(img, None, 1.0/viewScale, 1.0/viewScale )

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
		cv2.putText( img2, str(iterIdx), (10,20), font, 1.0, (0,250,250) )

		print( "Found ", face.shape[0], " face" )
#		print( " shape r=", face.shape[0], " shape c=", face.shape[1] )
		for (x, y, w, h) in face:
			x=int(x/viewScale)
			y=int(y/viewScale)
			w=int(w/viewScale)
			h=int(h/viewScale)
			cv2.putText( img2, str(w)+"x"+str(h), (x,y), font, 1.0, (0,250,250) )
			cv2.rectangle(img2, (x, y), (x + w, y + h), (128, 255, 0), 2)
			deltax=w/3
			deltay=h/2
			x0 = int( x - deltax   )
			y0 = int( y - deltay   )
			w0 = int( w + 2*deltax )
			h0 = int( h + 2*deltay )
			cv2.rectangle(img2, (x0, y0), (x0 + w0, y0 + h0), (255, 255, 0), 2)

	cv2.imshow(window,img2)

#=====================================================================
# TRACKBAR CALLBACK FUNCTIONS

# scaleFactor
def on_trackbar_sf(val):
	if iterIdx != 0:
		scaleFactor = val / 10
		print( "scale factor=", scaleFactor )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )

# minNeighbors
def on_trackbar_mn(val):
	if iterIdx != 0:
		minNeighbors = val
		print( "minNeighbors=", minNeighbors )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )

# minSize
def on_trackbar_min(val):
	if iterIdx != 0:
		minBBsize = val
		print( "minBBsize=", minBBsize )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )

# maxSize
def on_trackbar_max(val):
	if iterIdx != 0:
		maxBBsize = val
		print( "maxBBsize=", maxBBsize )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )


#=====================================================================
# BEGIN

import tkinter
app = tkinter.Tk()
s_width  = app.winfo_screenwidth()-100
s_height = app.winfo_screenheight()-250

if( len(sys.argv) != 2 ):
	print( "Error, require 1 argument: filename" )
	exit(1)
	
fullfname = sys.argv[1]

img_src = cv2.imread(fullfname)
if img_src is None:
	print( "failed to read image, quitting..." )
	exit(2)
	
print( "input image size=", img_src.size, " size=", img_src.shape, "w=", img_src.shape[1]  )

im_w = img_src.shape[1]
im_h = img_src.shape[0]

if (im_w>s_width or im_h>s_height):
	k_w = im_w/s_width
	k_h = im_h/s_height
	print("k_w=",k_w, " k_h=", k_h )
	viewScale=k_w
	if k_h>k_w:
		viewScale=k_h
	print("view scale factor=", viewScale ) 

	
gray_image = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

cv2.namedWindow(window)

cv2.createTrackbar( "Scale Factor",  window , int(scaleFactor*10), 50, on_trackbar_sf)
cv2.createTrackbar( "min Neighbors", window , minNeighbors,        40, on_trackbar_mn)
cv2.createTrackbar( "min size",      window , minBBsize,           minBBsize*10, on_trackbar_min )
cv2.createTrackbar( "max size",      window , maxBBsize,           int(img_src.shape[1]/2), on_trackbar_max )


while True:
	processDetection()
	key=cv2.waitKey(0)
	if key == 27:
		break

