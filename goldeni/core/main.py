#!/usr/bin/python

import algorithms
import os
import Image
import cv
from math import ceil

class main:

	def pilToCV(self,inImage):
		cv_im = cv.CreateImageHeader(inImage.size, cv.IPL_DEPTH_8U, 1)	
		cv.SetData(cv_im, inImage.tostring())
		return cv_im

	def CVTopil(self,inImage):
		cv_im = cv.CreateImage(cv.GetSize(inImage), cv.IPL_DEPTH_8U, 1)
		PILImage = Image.fromstring("L", cv.GetSize(cv_im), cv_im.tostring())
		return PILImage

	def __init__(self,path):
		# Image name
		name = os.path.basename(path)

		# Open image
		inputImage = Image.open(path)

		# If image is not 8-bit, grayscale it
		grayImageObject = algorithms.grayscaledImage(inputImage)
		grayscaleImage = grayImageObject.grayImage
		#grayscaleImage.save("out/gray-" + name)

		# Blur the image (the blur radius should depend on the size of the image, fix that)
		blurredImageObject = algorithms.blurredImage(grayscaleImage)
		blurredImage = blurredImageObject.blurImage
		#blurredImage.save("out/blur-" + name)

		# Threshold to find pupil
		thresholdedImageObject = algorithms.thresholdedImage(blurredImage,0,70)
		self.thresholdedImage = thresholdedImageObject.thresholdImage
		self.pupilThreshold = thresholdedImageObject.thr
		print "Threshold is %s" % self.pupilThreshold


		self.thresholdedImage.save("out/thresh-" + name)


		CannyHoughObject = algorithms.CannyHough(self.thresholdedImage,35)
		self.xPoint = int(CannyHoughObject.x)
		self.yPoint = int(CannyHoughObject.y)
		self.rPoint = int(ceil(CannyHoughObject.r))

		#########Testing - Display pupil circle in output image###########
		cv_im = self.pilToCV(self.thresholdedImage)	
		dst = cv.CreateImage(inputImage.size,cv.IPL_DEPTH_8U,3)
		cv.CvtColor(cv_im,dst,cv.CV_GRAY2RGB)
		cv.Circle(dst,(self.xPoint,self.yPoint),self.rPoint,cv.RGB(255, 0, 0),1,2)
		cv.SaveImage("out/circle-"+name,dst)

		##################################################################
	
		###Test for iris boundary detection###
		### This is slightly more complicated than the pupil detection
		### What we will do it look for the second peak in the histogram,
		### then search around that threshold for the optimal value
		#####EVENTUALLY MOVE TO ALGORITHMS CLASS
		#####Make threshold class only fot otsu
		print "Threshold before is %s" % thresholdedImageObject.thr
		hist = blurredImage.histogram()
		firstMax = -1
		firstMaxIndex = -1
		for t in range(70,240):
			if hist[t] > firstMax:
				firstMax = hist[t]
				firstMaxIndex = t
		secondMax = -1
		secondMaxIndex = -1
		for t in range(firstMaxIndex + 20,240):
			if hist[t] > secondMax:
				secondMax = hist[t]
				secondMaxIndex = t
		for t in range(70, firstMaxIndex - 20):
			if hist[t] > secondMax:
				secondMax = hist[t]
				secondMaxIndex = t

		if firstMaxIndex > secondMaxIndex:
			tmp = firstMaxIndex
			firstMaxIndex = secondMaxIndex
			secondMaxIndex = tmp

		tmin = firstMax
		minIndex = -1
		for t in range(firstMaxIndex,secondMaxIndex):
			if hist[t] < tmin:
				tmin = hist[t];
				minIndex = t
		print "New Threshold: ",minIndex

		lut = [255 if v > minIndex else 0 for v in range(256)]
	
		threshold2Image = blurredImage.point(lut)

		threshold2Image.save("out/thresh2-" + name)

		CannyHoughObject2 = algorithms.CannyHough(threshold2Image,int(self.rPoint*1.5))
		self.x2Point = int(CannyHoughObject2.x)
		self.y2Point = int(CannyHoughObject2.y)
		self.r2Point = int(ceil(CannyHoughObject2.r))

		#########Testing - Display pupil circle in output image###########
		cv.Circle(dst,(self.x2Point,self.y2Point),self.r2Point,cv.RGB(0, 255, 0),1,2)
		cv.SaveImage("out/circle2-"+name,dst)

		##################################################################

		#self.thresholded2Image = thresholded2ImageObject.thresholdImage
		#firstMax = thresholded2ImageObject.t - 4
		#print "Firstmax is %s" % firstMax
		#thresholded3ImageObject = algorithms.thresholdedImage(blurredImage,firstMax + 20,240)
		#secondMax = thresholded3ImageObject.t - 4
		#thresholded4ImageObject = algorithms.thresholdedImage(blurredImage,firstMax - 20,240)
		#self.thresholded2Image.save("out/thresh2-" + name)

		

