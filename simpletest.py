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

ip = "10.20.16.2"
points = [(240,0),(240,640)]
NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

class ThisClient(object):
	'''this is a test client'''
	turretAngle = ntproperty('/SmartDashboard/turretAngle',0,writeDefault=False)
	xCoord = ntproperty('/SmartDashboard/xCoord',0)
	yCoord = ntproperty('/SmartDashboard/yCoord',0)

c = ThisClient()


while TRUE:
	imgA = usbCam.getImage()

	hsvImg = imgA.toHSV()
	output  = imgA/5
	output = output.binarize(50).morphOpen().invert()
	blobs = output.findBlobs()
	layer = DrawingLayer((imgA.width,imgA.height))
	layer.line((320,0),(320,480),color=Color.RED,width=3) 
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
			output = imgA
	output.addDrawingLayer(layer)
	output.applyLayers()
	output.save(js)
     	c.xCoord = xCenter
     	c.yCoord = yCenter		
	time.sleep(0.01)
