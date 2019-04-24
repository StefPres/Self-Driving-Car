# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
from pyzbar import pyzbar
import numpy as np
import argparse
import cv2
import imutils
import time
import serial


arduino = serial.Serial('/dev/ttyACM0', 115200)
horiz = ""
vert = ""

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
ap.add_argument("-f", "--fps", type=int, default=32, help="Framerate")
ap.add_argument("-x", "--horizontal", type=int, default=480, help="Horizontal screen size")
ap.add_argument("-y", "--vertical", type=int, default=360, help="Vertical screen size")
ap.add_argument("-s", "--size", type=int, default=8, help="Object Size")
args = vars(ap.parse_args())


# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
counter = 0
(dX, dY) = (0, 0)
direction = ""
screenx = args["horizontal"]
screeny = args["vertical"]
code = []
codestring = ""


# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    print "grabbing video"
    #vs = VideoStream(src=0).start()
    camera = PiCamera()
    camera.resolution = (screenx, screeny)
    camera.framerate = args["fps"]
    rawCapture = PiRGBArray(camera, size=(screenx, screeny))

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    # handle the frame from VideoCapture or VideoStream
    #frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        print "broke while loop"
        break


    # resize the frame, blur it, and convert it to the HSV
    # color space
	barcodes = pyzbar.decode(frame)
   for barcode in barcodes:
	codestring = "" # reset the codestring
	# extract the bounding box location of the barcode and draw the
	# bounding box surrounding the barcode on the image
	(x, y, w, h) = barcode.rect
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
	# the barcode data is a bytes object so if we want to draw it on
	# our output image we need to convert it to a string first
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type
        text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	# only proceed if the radius meets a minimum size
        code = barcodeData.split() # Code format is DIRx PWRxxx TRNx TRRx TRTx
	
	for i in range(0, 5, 1):
		stuff = code[i]
		codestring += stuff[2, len.stuff]
        
	arduino.write(codestring)


    # show the frame to our screen and increment the frame counter
    #cv2.imshow("Frame", frame)
    #key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop
    #if key == ord("q"):
    #   break
    rawCapture.truncate(0)

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
#cv2.destroyAllWindows()
