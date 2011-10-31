#!/usr/bin/python

import algorithms
import os
import Image
import cv
from math import ceil

class main:
	def __init__(self,path):
		# Image name
		name = os.path.basename(path)

		# Open image
		inputImage = Image.open(path)

		# If image is not 8-bit, grayscale it
		grayImageObject = algorithms.grayscaledImage(inputImage)
		grayscaleImage = grayImageObject.grayImage
		grayscaleImage.save("out/gray-" + name)

		# Blur the image (the blur radius should depend on the size of the image, fix that)
		blurredImageObject = algorithms.blurredImage(grayscaleImage)
		blurredImage = blurredImageObject.blurImage
		blurredImage.save("out/blur-" + name)

		# Threshold to find pupil
		thresholdedImageObject = algorithms.thresholdedImage(blurredImage,0)
		self.thresholdedImage = thresholdedImageObject.thresholdImage
		self.pupilThreshold = thresholdedImageObject.thr
		print "Threshold is %s" % self.pupilThreshold


		self.thresholdedImage.save("out/thresh-" + name)


		CannyHoughObject = algorithms.CannyHough(self.thresholdedImage)
		#CannyCircleImage = CannyHoughObject.cvPupil
		self.xPoint = int(CannyHoughObject.x)
		self.yPoint = int(CannyHoughObject.y)
		self.rPoint = int(ceil(CannyHoughObject.r))

		#########Testing###########
		cv_im = cv.CreateImageHeader(self.thresholdedImage.size, cv.IPL_DEPTH_8U, 1)	
		cv.SetData(cv_im, self.thresholdedImage.tostring())
		dst = cv.CreateImage(inputImage.size,cv.IPL_DEPTH_8U,3)
		cv.CvtColor(cv_im,dst,cv.CV_GRAY2RGB)
		cv.Circle(dst,(self.xPoint,self.yPoint),self.rPoint,cv.RGB(255, 0, 0),1,2)
		cv.SaveImage("out/circle-"+name,dst)

		###########################
		#print CannyHoughObject.cvSize
		#print CannyHoughObject.storage
	
		###Test for iris boundary detection###
		print "Threshold before is %s" % thresholdedImageObject.thr
		thresholded2ImageObject = algorithms.thresholdedImage(blurredImage,self.pupilThreshold+50)
		self.thresholded2Image = thresholded2ImageObject.thresholdImage
		print "Threshold is %s" % thresholded2ImageObject.thr
		self.thresholded2Image.save("out/thresh2-" + name)



