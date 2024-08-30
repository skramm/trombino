#!/usr/bin/env python3

# GUI app, designed to manually find correct parameters for face detection

# 1 argument required: full filename

#----------------------------------------------
# Default Parameters, will be adjusted with trackbars
# see https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html

# will be adjusted to 1/20 of image width
tb_minBBsize=60
# will be adjusted to 1/2 of image width
tb_maxBBsize=120

tb_scaleFactor=2.0
tb_minNeighbors=5
#----------------------------------------------

import os
import sys
import cv2
import pathlib
from pathlib import Path

# used to adapt large images to the screen
viewScale=1.0

window="calib"
font = cv2.FONT_HERSHEY_SIMPLEX
iterIdx=0
img=None
img2=None
line=30

def printValue( img, txt):
	global line	
	cv2.putText( img2, txt, (10,line), font, 0.6, (0,250,250) )
	line=line+20

#=====================================================================
# main detection function
def processDetection():
	global iterIdx,img2,line
	iterIdx=iterIdx+1
	line=30
	img = img_src.copy()

	img2 = cv2.resize(img,  (int(img.shape[1]/viewScale), int(img.shape[0]/viewScale )))
	printValue( img2, str(im_w)+"x"+ str(im_h) )
	printValue( img2, "viewScale="+str(viewScale) )
	printValue( img2, "scale="+str(tb_scaleFactor) )
	printValue( img2, "minNeighbors="+str(tb_minNeighbors) )
	printValue( img2, "minBBsize="+str(tb_minBBsize) )
	printValue( img2, "maxBBsize="+str(tb_maxBBsize) )

# this does not work, but it should! (?)
# see https://docs.opencv.org/4.6.0/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d
#	img2 = cv2.resize(img, None, 1.0/viewScale, 1.0/viewScale )

	face = face_classifier.detectMultiScale(
		gray_image
		,scaleFactor=tb_scaleFactor
		,minNeighbors=tb_minNeighbors
		,minSize=(tb_minBBsize, tb_minBBsize)
		,maxSize=(tb_maxBBsize, tb_maxBBsize)
	)
	if len(face) == 0:
		print( "Failed to find face!")
	else:
		print( "Found", face.shape[0], "face" )
		idx=0
		for (x, y, w, h) in face:
			print( " -face",idx,": ", face[idx] )
			x1=int(x/viewScale)
			y1=int(y/viewScale)
			w1=int(w/viewScale)
			h1=int(h/viewScale)
			cv2.putText( img2, str(w)+"x"+str(h), (x1,y1), font, 1.0, (0,250,250) )
			cv2.rectangle(img2, (x1, y1), (x1 + w1, y1 + h1), (128, 255, 0), 2)
			deltax=w1/3
			deltay=h1/2
			x0 = int( x1 - deltax   )
			y0 = int( y1 - deltay   )
			w0 = int( w1 + 2*deltax )
			h0 = int( h1 + 2*deltay )
			cv2.rectangle(img2, (x0, y0), (x0 + w0, y0 + h0), (255, 255, 0), 2)
			idx=idx+1

	cv2.imshow(window,img2)

#=====================================================================
# TRACKBAR CALLBACK FUNCTIONS

# scaleFactor
def on_trackbar_sf(val):
	if iterIdx != 0:
		global tb_scaleFactor
		tb_scaleFactor = (val+11) / 10
#		print( "scale factor=", tb_scaleFactor )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )

# minNeighbors
def on_trackbar_mn(val):
	if iterIdx != 0:
		global tb_minNeighbors
		tb_minNeighbors = val
#		print( "minNeighbors=", tb_minNeighbors )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )

# minSize
def on_trackbar_min(val):
	if iterIdx != 0:
		global tb_minBBsize
		tb_minBBsize = val
#		print( "minBBsize=", tb_minBBsize )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )
'''
# maxSize
def on_trackbar_max(val):
	if iterIdx != 0:
		global tb_maxBBsize
		tb_maxBBsize = val
		print( "maxBBsize=", tb_maxBBsize )
		processDetection()
		if img != None: 
			cv2.imshow( window, img2 )
'''

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

tb_minBBsize=int(img_src.shape[1]/20)
tb_maxBBsize=int(img_src.shape[1]/2)

cv2.namedWindow(window)

cv2.createTrackbar( "Scale Factor",  window , int(tb_scaleFactor*10), 50, on_trackbar_sf)
cv2.createTrackbar( "min Neighbors", window , tb_minNeighbors,        40, on_trackbar_mn)
cv2.createTrackbar( "min size",      window , tb_minBBsize,           int(img_src.shape[1]/2), on_trackbar_min )
#cv2.createTrackbar( "max size",      window , tb_maxBBsize,           int(img_src.shape[1]/2), on_trackbar_max )

face_classifier = cv2.CascadeClassifier(
	cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while True:
	processDetection()
	key=cv2.waitKey(0)
	if key == 27:
		break

