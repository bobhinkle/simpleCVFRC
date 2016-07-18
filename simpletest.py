//This code opens the usb camera at the default resolution
//It also creates a jpegstreamer to view the image after it is processed
//You will need to change the ip to match your robot ip
//This is not using any color tricks yet. It is just using the pricinpal that we are going to send it an image with retroreflective
//tape. 

import sys
import time

from SimpleCV import *
from networktables import NetworkTable
from networktables.util import ntproperty

showColor = FALSE

usbCam = Camera()

js = JpegStreamer("0.0.0.0.:8080",0.01)
print(js.url())
print(js.streamUrl())

xCenter = 0
yCenter = 0

ip = "10.20.16.2"  //change this to match your robot ip address
points = [(240,0),(240,640)]
NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

class ThisClient(object):
	'''this is a test client'''
	turretAngle = ntproperty('/SmartDashboard/turretAngle',0,writeDefault=False)
	xCoord = ntproperty('/SmartDashboard/xCoord',0) //this is sent to smart dashboard
	yCoord = ntproperty('/SmartDashboard/yCoord',0)

c = ThisClient()


while TRUE:
	imgA = usbCam.getImage()  //This sets imgA to the image from camera
	hsvImg = imgA.toHSV()  //converts the image to HSV
	output  = imgA/5    //Darkens the image. increase the demoninator to darken image
	output = output.binarize(50).morphOpen().invert() //inverts the image. SimpleCV likes white to be the target image
	blobs = output.findBlobs()  //finds objects in the image
	layer = DrawingLayer((imgA.width,imgA.height)) //creates a layer to draw on
	layer.line((320,0),(320,480),color=Color.RED,width=3) //puts a red dot on the center of the target
	if blobs:
		items = blobs.count()
		maxArea = 0
		while items > -1:
			if blobs[items-1].length() > maxArea:
				maxArea = items
		layer.circle((blobs[maxArea-1].x,blobs[maxArea-1].y),5,color=Color.RED,filled=True)
		xCenter = blobs[maxArea-1].x
		yCenter = blobs[maxArea-1].y
	if showColor:
		output = imgA  //if this is false it will display the HSV image. If true it just displays the red dot over full image
	output.addDrawingLayer(layer)
	output.applyLayers()
	output.save(js)
     	c.xCoord = xCenter
     	c.yCoord = yCenter		
	time.sleep(0.01) //delay the process. There is a lag running at 640x480. I haven't tried lower resolutions
