#!/usr/bin/env python3

# src: https://www.datacamp.com/tutorial/face-detection-python-opencv

# 2 arguments required
# -1: output folder
# -2: filename (with path, say "my/folder/photo_12345.jpg")

#----------------------------------------------
# PARAMETERS (adjust if needed)
# see https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html
minBBsize=50
scale=1.5
#----------------------------------------------


import os
import sys
import cv2
import pathlib
from pathlib import Path

#import matplotlib.pyplot as plt

#print( "nb arg=",len(sys.argv) )
if( len(sys.argv) != 3 ):
	print( "Error, require 2 arguments" )
	exit(1)
	
dir_out = sys.argv[1]
fullfname = sys.argv[2]
fname = os.path.basename(fullfname)

img = cv2.imread(fullfname)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print( "input image size=", img.size, " size=", img.shape )

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

face = face_classifier.detectMultiScale(
    gray_image, scaleFactor=scale, minNeighbors=5, minSize=(minBBsize, minBBsize)
)

print( "nd rect=", face )
print( "size=", face.size, " ndim=", face.ndim, " shape=", face.shape )
print( " shape r=", face.shape[0], " shape c=", face.shape[1] )

if( face.shape[0] != 1 ):
	print( "Failure, found ", face.shape[0], " faces in file ", sys.argv[1] )
	exit(1)

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



