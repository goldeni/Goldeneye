#!/usr/bin/python

import algorithms
import threshold 
import os
import Image
import hough
from math import pow,sqrt
import sys
import imgUtils
import glob
import time
import matplotlib.pyplot as plt

class main:
	def __init__(self,path):
		# Start timing construct
		initTime = time.time()

		print "Processing iris"

		# Image name
		name = os.path.basename(path)
		print "File: ",name

		# Open image
		inputImage = Image.open(path)
		w,h = inputImage.size
		print "Size = ",w,h

		preGS = time.time()
		# If image is not 8-bit, grayscale it
		grayImageObject = algorithms.grayscaledImage(inputImage)
		grayscaleImage = grayImageObject.grayImage
		#grayscaleImage.save("out/gray-" + name)
		GStime = time.time() - preGS
		print "It took %.3f" % (1000 * GStime),"ms\n\n\n"

		preB = time.time()
		# Blur the image (the blur radius should depend on the size of the image, fix that)
		blurredImageObject = algorithms.blurredImage(grayscaleImage,11)
		blurredImage = blurredImageObject.blurImage
	#	blurredImage.save("out/blur-" + name)
		Btime = time.time() - preB
		print "Blurring Done"
		print "It took %.3f" % (1000 * Btime),"ms\n\n\n"

		prePT = time.time()
		hist = blurredImage.histogram()
		ind = range(256)
		plt.bar(ind,hist)
		plt.show()
		threshObj = threshold.threshold(hist)
		pupilThreshold = threshObj.pupilThresh(0,70)
		lut = [255 if v > pupilThreshold else 0 for v in range(256)]
	
		pupilThreshImage = blurredImage.point(lut)
		pupilThreshImage.save("out/thresh1-" + name)
		PTtime = time.time() - prePT
		print "Threshold 1 saved"
		print "It took %.3f" % (1000 * PTtime),"ms\n\n\n"

		pupilPixels = pupilThreshImage.load()


########################################################
		preB2 = time.time()
		iBlurredImageObject = algorithms.blurredImage(grayscaleImage,3)
		iBlurredImage = blurredImageObject.blurImage
		B2time = time.time() - preB2
		print "Blurring pt 2 Done"
		print "It took %.3f" % (1000 * B2time),"ms\n\n\n"

		print "Threshold before is %s" % pupilThreshold
		irisThresh = threshObj.irisThresh(pupilThreshold,240)
#		irisThresh = 90

		lut = [255 if v > irisThresh else 0 for v in range(256)]

		irisThreshImage = iBlurredImage.point(lut)
		irisThreshImage.save("out/thresh2-" + name)
		print "Threshold 2 saved"

###########################################################

		SobelPupilObject = algorithms.sobelFilter(pupilThreshImage)
		SobelPupilImage = SobelPupilObject.outputImage
		SobelPupilImage.save("out/sobelpupil-"+name)

		SobelIrisObject = algorithms.sobelFilter(irisThreshImage)
		SobelIrisImage = SobelIrisObject.outputImage

		prePH = time.time()
		print "Testing threshold and determining bounding box for pupil..."
		sumx = 0
		sumy = 0
		amount = 0

		for x in range(10,w):
			for y in range(10,h):
				if pupilPixels[x,y] == 0:
					sumx += x
					sumy += y
					amount += 1

		if sumx == 0 or sumy == 0:
			print "Sorry brah, the pupil's gone"
			sys.exit()

		sumx /= amount
		sumy /= amount

		pupilBoxCenter = (sumx, sumy)

		radius = sumx
		print "Initial radius: ",radius
		while pupilPixels[radius,sumy] == 0:
			radius += 1
		radius -= sumx - 2

		print "Final radius = ",radius

		print "Done"
		HoughObject = hough.HoughTransform(SobelPupilImage,(sumx-1,sumy-1),(4,4),radius-4,radius+4)
		pP0 = HoughObject.circle0
		pP1 = HoughObject.circle1
		pP2 = HoughObject.circle2

		pX = HoughObject.topx
		pY = HoughObject.topy
		pR = HoughObject.topr

		PHtime = time.time() - prePH
		print "\n\n\nPupil Circle Fit Done"
		print "It took %.3f" % (1000 * PHtime),"ms\n\n\n"
		#################abstract into function or something
		if pP0 == pP1 or pP1 == pP2 or pP0 == pP2:
			print "error"
			sys.exit()
		
		print "pP0 = ",pP0
		print "pP1 = ",pP1
		print "pP2 = ",pP2

		pupilDrawObject = imgUtils.Utils(inputImage)
		pupilDraw = pupilDrawObject.drawCircle(pP0[0],pP0[1],5)
		pupilDraw = pupilDrawObject.drawCircle(pP1[0],pP1[1],5)
		pupilDraw = pupilDrawObject.drawCircle(pP2[0],pP2[1],5)
		pupilDraw = pupilDrawObject.drawCircle(pX,pY,109)
		pupilDraw = pupilDrawObject.drawCircle(pX,pY,pR)

		#ht = ((pow(pP0[0],2) + pow(pP0[1],2)) * (pP1[1] - pP2[1]) + (pow(pP1[0],2) + pow(pP1[1],2)) * (pP2[1] - pP0[1]) + (pow(pP2[0],2) + pow(pP2[1],2)) * (pP0[1] - pP1[1])) / (2 * (pP0[0] * pP1[1] - pP1[0] * pP0[1] - pP0[0] * pP2[1] + pP2[0] * pP0[1] - pP2[0] * pP1[1]))
		#k = ((pow(pP0[0],2) + pow(pP0[1],2)) * (pP2[0] - pP1[0]) + (pow(pP1[0],2) + pow(pP1[1],2)) * (pP0[0] - pP1[0]) + (pow(pP2[0],2) + pow(pP2[1],2)) * (pP1[0] - pP0[0])) / (2 * (pP0[0] * pP1[1] - pP1[0] * pP0[1] - pP0[0] * pP2[1] + pP2[0] * pP0[1] - pP2[0] * pP1[1]))

		ht,k = self.calcCircleCenter(pP0,pP1,pP2)
		print "Pupil Center: ",ht,k,pP0,pP1
		print "Real Pupil Center: ",pX,pY,pR

		pupilDraw = pupilDrawObject.drawCircle(ht,k,3)
		pupilDraw.save("out/pupil-pP2-" + name)

		tL = (pX-5,pY-5)
		bR = (pX+5,pY+5)

		xR = pP0[0] - ht
		yR = pP0[1] - k
		rR = sqrt(pow(xR,2) + pow(yR,2))

		print tL,bR,rR

		inRad = rR

		SobelIrisImage.save("out/sobel2-" + name)

		irisEdgesObject = hough.HoughTransform(SobelIrisImage,tL,bR,w/4,h/2)
		iP0 = irisEdgesObject.circle0
		iP1 = irisEdgesObject.circle1
		iP2 = irisEdgesObject.circle2

		xPR = iP0[0] - ht
		yPR = iP0[1] - k
		outRad = sqrt(pow(xPR,2) + pow(yPR,2))

		print "Iris: ",ht,k,inRad,outRad

		irisDrawObject = imgUtils.Utils(inputImage)
		print "Woah, this is heavy"
		print ht,k,inRad,outRad
		irisDraw = irisDrawObject.drawCircle(pX,pY,irisEdgesObject.topr)
		
		inputImage.save("out/circle1-" + name)

		#HoughObject2 = hough.HoughTransform(SobelPupilImage,90,170,"",xPoint,yPoint)
		##(xPoint2,yPoint2,rPoint2) = HoughObject2.circle
		##circle2 = imgUtils.Utils(inputImage)
		##circle2Image = circle1.drawCircle(xPoint2,yPoint2,rPoint2)
		
		##circle2Image.save("out/circle2-" + name)
		#box2 = (xPoint2-rPoint2,yPoint2-rPoint2,xPoint2+rPoint2,yPoint2+rPoint2)

		#circle2 = ImageDraw.Draw(inputImage)
		#circle2.ellipse(box2,outline=255)
		#del circle2

		#inputImage.save("out/circle2-" + name)

	def calcCircleCenter(self,a,b,c):
		a0 = a[0] * a[0]
		b0 = b[0] * b[0]
		c0 = c[0] * c[0]
		a1 = a[1] * a[1]
		b1 = b[1] * b[1]
		c1 = c[1] * c[1]
		axy = a0+a1
		bxy = b0+b1
		cxy = c0+c1
		denom = 2*((a[0]*b[1])-(b[0]*a[1])-(a[0]*c[1])+(c[0]*a[1])+(b[0]*c[1])-(c[0]*b[1]))

		ht = (axy * (b[1] - c[1]) + bxy * (c[1] - a[1]) + cxy * (a[1] - b[1])) / denom
		k = (axy * (c[0] - b[0]) + bxy * (a[0] - b[0]) + cxy * (b[0] - a[0])) / denom
		return int(ht),int(k)

if __name__ == "__main__":
	argc = len(sys.argv)
	for i in range(1,argc):
		main(sys.argv[i])

