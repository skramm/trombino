#!/usr/bin/env python3

# interactive version, if no face is found, will ask for
# manual parameter adjustement with trackbars

# src: https://www.datacamp.com/tutorial/face-detection-python-opencv

# 2 arguments required
# -1: filename (with path, say "my/folder/photo_12345.jpg")
# -2: output folder

#----------------------------------------------
# PARAMETERS (adjust if needed)
# see https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html
minBBsize=60
scale=2.0
#----------------------------------------------


import os
import sys
import cv2
import pathlib
import tkinter
from pathlib import Path

img_src=None
img2=None
im_w=200
im_h=200
viewScale=1.0
gray_image=None
tb_scaleFactor=2.0
tb_minNeighbors=5
iterIdx = 0
line = 30
font = cv2.FONT_HERSHEY_SIMPLEX
guiMode=False

tb_minBBsize=60
tb_maxBBsize=120
tb_scaleFactor=2.0
tb_minNeighbors=5

window="GUI"

#---------------------------------------------------------------------
# Helper function, to print values on image
def printValue( img, txt):
	global line	
	cv2.putText( img, txt, (10,line), font, 0.6, (0,250,250) )
	line=line+20

#=====================================================================
def drawStuff():
	global line,img2,im_w,im_h
	line=30
	img2 = cv2.resize(img_src,  (int(img_src.shape[1]/viewScale), int(img_src.shape[0]/viewScale )))

	printValue( img2, str(iterIdx) )
	printValue( img2, str(im_w)+"x"+ str(im_h) )
	printValue( img2, "viewScale="+str(viewScale) )
	printValue( img2, "scale="+str(tb_scaleFactor) )
	printValue( img2, "minNeighbors="+str(tb_minNeighbors) )
	printValue( img2, "minBBsize="+str(tb_minBBsize) )
	printValue( img2, "maxBBsize="+str(tb_maxBBsize) )

#=====================================================================
# TRACKBARS CALLBACK FUNCTIONS

# scaleFactor
def on_trackbar_sf(val):
	print("on_trackbar_sf iter=", iterIdx)
	global tb_scaleFactor
	tb_scaleFactor = (val+11) / 10
	print( "scale factor=", tb_scaleFactor )
	processDetection()
	drawStuff()
	cv2.imshow( window, img2 )

# minNeighbors
def on_trackbar_mn(val):
	print("on_trackbar_mn iter=", iterIdx)
#	if iterIdx != 0:
	global tb_minNeighbors
	tb_minNeighbors = val
	print( "minNeighbors=", tb_minNeighbors )
	processDetection()
	drawStuff()
	cv2.imshow( window, img2 )

def on_trackbar_minBB(val):
	print("on_trackbar_minBB=", iterIdx)
#	if iterIdx != 0:
	global tb_minBBsize
	tb_minBBsize = val
	print( "tb_minBBsize=", tb_minBBsize )
	processDetection()
	drawStuff()
	cv2.imshow( window, img2 )


#=====================================================================
def saveCroppedImage( face ):
	deltax=face[0][2]/3
	deltay=face[0][2]/2
	x0 = int( face[0][0] - deltax   )
	y0 = int( face[0][1] - deltay   )
	w0 = int( face[0][2] + 2*deltax )
	h0 = int( face[0][3] + 2*deltay )

	#cv2.rectangle(img, (x0, y0), (x0 + w0, y0 + h0), (0, 255, 0), 4)

	img_out = gray_image[y0:y0+h0,x0:x0+w0]
	cv2.imwrite(dir_out+"/"+fname,img_out)

#=====================================================================
# main detection function
def processDetection():
	global iterIdx
	iterIdx=iterIdx+1
#	global iterIdx,img2,line
	
#	line=30
#	if guiMode == True:
#		img = img_src.copy()


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
		print( "Found face:", face )
	return face

#=====================================================================
# start the GUI and wait for interaction
def startGUI():
	global guiMode,img_src,iterIdx,viewScale,im_w,im_h
	guiMode=True
	
	app = tkinter.Tk()
	s_width  = app.winfo_screenwidth()-100
	s_height = app.winfo_screenheight()-250
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

	img2 = cv2.resize(img_src,  (int(img_src.shape[1]/viewScale), int(img_src.shape[0]/viewScale )))

	cv2.namedWindow(window)
	cv2.createTrackbar( "Scale Factor",  window , int(tb_scaleFactor*10), 50,             on_trackbar_sf    )
	cv2.createTrackbar( "min Neighbors", window , tb_minNeighbors,        40,             on_trackbar_mn    )
	cv2.createTrackbar( "min BB size",   window , tb_minBBsize,           tb_minBBsize*2, on_trackbar_minBB )
	while True:
		print("loop start")
#		face=processDetection()
#		drawStuff()
#		img = img_src.copy()

		img2 = cv2.resize(img_src,  (int(img_src.shape[1]/viewScale), int(img_src.shape[0]/viewScale )))
		cv2.imshow(window,img2)
#		iterIdx=iterIdx+1
		key=cv2.waitKey(0)
		if key == 27:
			break
		if key == 32: # SPC
			if len(face) != 1:
				print("cannot proceed, face not unique")
			else:
				saveCroppedImage( face )
				print( "Cropped image saved, exiting")
				break;

#=====================================================================
# PROGRAM START

if( len(sys.argv) != 3 ):
	print( "Error, require 2 arguments" )
	exit(1)
	
fullfname = sys.argv[1]
dir_out = sys.argv[2]
fname = os.path.basename(fullfname)
print( "fullfname=", fullfname )

img_src = cv2.imread(fullfname)
if img_src is None:
	print( "failed to read image, quitting..." )
	exit(2)
	
print( "input image size=", img_src.size, " size=", img_src.shape )
gray_image = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

tb_minBBsize=int(img_src.shape[1]/20)
tb_maxBBsize=int(img_src.shape[1]/2)

face_classifier = cv2.CascadeClassifier(
	cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
face = processDetection()

print("face=",face)
if len(face) != 1:
	print( "Failed to find unique face, start interactive GUI" )
	startGUI()
else:
	saveCroppedImage( face )

#print( "nd rect=", face )
#print( "size=", face.size, " ndim=", face.ndim, " shape=", face.shape )
#print( " shape r=", face.shape[0], " shape c=", face.shape[1] )

#if( face.shape[0] != 1 ):
#	print( "Failure, found ", face.shape[0], " faces in file ", sys.argv[1] )
#	exit(4)

#for (x, y, w, h) in face:
#    cv2.rectangle(img, (x, y), (x + w, y + h), (128, 255, 0), 4)

	



