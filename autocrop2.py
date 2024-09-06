#!/usr/bin/env python3
'''
Interactive version of face auto-cropping:
if no face is found, will start a GUI (Openv-based) so
that user can test parameters. Once OK, press space, save image, and move on.
If no correct parameters can be found, just hit ESC, and image will be saved "as-is".

Based on: https://www.datacamp.com/tutorial/face-detection-python-opencv
 
- Green rectangle: actual detection
- Blue rectangle: the part that will be cropped 
'''

# 2 arguments min required
# -1: filename (with path, say "my/folder/photo_12345.jpg")
# -2: output folder


import os
import sys
import cv2
import pathlib
import tkinter
from pathlib import Path

appname="guicrop:"
img_src=None
img2=None
im_w=200
im_h=200
viewScale=1.0
gray_image=None
#face=None
iterIdx = 0
line = 30
font = cv2.FONT_HERSHEY_SIMPLEX


#----------------------------------------------
# Default parameters 
# see https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html

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
#	print("drawStuff()")
	global face,line,img2,im_w,im_h
	line=30
	img2 = cv2.resize(img_src,  (int(img_src.shape[1]/viewScale), int(img_src.shape[0]/viewScale )))

	printValue( img2, str(iterIdx) )
	printValue( img2, str(im_w)+"x"+ str(im_h) )
	printValue( img2, "viewScale="+str(viewScale) )
	printValue( img2, "scale="+str(tb_scaleFactor) )
	printValue( img2, "minNeighbors="+str(tb_minNeighbors) )
	printValue( img2, "minBBsize="+str(tb_minBBsize) )
	printValue( img2, "maxBBsize="+str(tb_maxBBsize) )

	if len(face) != 0:
		print( "drawStuff(): Found", face.shape[0], "face" )
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

#=====================================================================
# TRACKBARS CALLBACK FUNCTIONS

# scaleFactor
def on_trackbar_sf(val):
#	print("on_trackbar_sf iter=", iterIdx)
	if iterIdx != 1:
		global tb_scaleFactor
		tb_scaleFactor = (val+11) / 10
		print( "scale factor=", tb_scaleFactor )
		processDetection()
		drawStuff()
		cv2.imshow( window, img2 )

# minNeighbors
def on_trackbar_mn(val):
#	print("on_trackbar_mn iter=", iterIdx)
	if iterIdx != 1:
		global tb_minNeighbors
		tb_minNeighbors = val
		print( "minNeighbors=", tb_minNeighbors )
		processDetection()
		drawStuff()
		cv2.imshow( window, img2 )

def on_trackbar_minBB(val):
#	print("on_trackbar_minBB=", iterIdx)
	if iterIdx != 1:
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

	print( "cropped:", x0, y0, w0, h0, "name=", dir_out+"/"+fname )
	if (x0<0 or y0<0):
		print( "ERREUR: coordonnées négative, relancer avec l'option -m" )
		exit(6)
	
	img_out = gray_image[y0:y0+h0,x0:x0+w0]
	print( "im size=", img_out.size, " shape=", img_out.shape )
	cv2.imwrite(dir_out+"/"+fname,img_out)

#=====================================================================
# main detection function
def processDetection():
	global iterIdx,face
#	print("processDetection(): start", iterIdx)
	iterIdx=iterIdx+1

	face = face_classifier.detectMultiScale(
		gray_image
		,scaleFactor=tb_scaleFactor
		,minNeighbors=tb_minNeighbors
		,minSize=(tb_minBBsize, tb_minBBsize)
		,maxSize=(tb_maxBBsize, tb_maxBBsize)
	)
	if len(face) == 0:
		print( "processDetection(): Failed to find face!")
	else:
		print( "processDetection(): Found face:", face )
#	return face

#=====================================================================
# start the GUI and wait for interaction
def startGUI():
	global img_src,iterIdx,viewScale,im_w,im_h,face
	print("START GUI()");
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
	cv2.moveWindow(window,int(s_width/3),0)
	cv2.createTrackbar( "Scale Factor",  window , int(tb_scaleFactor*10), 50,             on_trackbar_sf    )
	cv2.createTrackbar( "min Neighbors", window , tb_minNeighbors,        40,             on_trackbar_mn    )
	cv2.createTrackbar( "min BB size",   window , tb_minBBsize,           tb_minBBsize*3, on_trackbar_minBB )
	while True:
		processDetection()
		drawStuff()
		cv2.imshow(window,img2)
		key=cv2.waitKey(0)
		if key == 27:
			break
		if key == 32: # SPC
			if len(face) != 1:
				print("Error, cannot proceed, face not unique")
			else:
				saveCroppedImage( face )
				print( "Cropped face image saved, exiting")
				break;

#=====================================================================
# PROGRAM START

print( "Installed Opencv version:", cv2.__version__ )
if( len(sys.argv) < 3 ):
	print( "Error, require 2 arguments" )
	exit(1)

fullfname = sys.argv[1]
dir_out = sys.argv[2]

print( appname, "argv=", len(sys.argv) )

manualmode = False
if sys.argv[1] == "-m":
	print( appname, "Manual mode for all")
	fullfname = sys.argv[2]
	manualmode = True
	if( len(sys.argv) < 4 ):
		print( "Error, require output folder")
		exit(1)
	dir_out = sys.argv[3]
	
fname = os.path.basename(fullfname)

img_src = cv2.imread(fullfname)
if img_src is None:
	print( "failed to read image '"+fullfname+"', quitting..." )
	exit(2)


print( "input image: w=", img_src.shape[1], "h=", img_src.shape[0] )
gray_image = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

# default minimum BB size: 1/20 of image width
tb_minBBsize=int(img_src.shape[1]/20)
# max BB size: half of width
tb_maxBBsize=int(img_src.shape[1]/2)

face_classifier = cv2.CascadeClassifier(
	cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
processDetection()

if manualmode:
	startGUI()
else:
	if len(face) != 1:
		print( "Failed to find unique face, start interactive GUI" )
		startGUI()
	else:
		saveCroppedImage( face )


