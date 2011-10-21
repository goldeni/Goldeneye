#!/usr/bin/python

import algorithms
import os
import Image
import cv

class main:
	def __init__(self,path):
		name = os.path.basename(path)
		inputImage = Image.open(path)

		grayImageObject = algorithms.grayscaledImage(inputImage)
		grayscaleImage = grayImageObject.grayImage
		grayscaleImage.save("out/gray-" + name)

		blurredImageObject = algorithms.blurredImage(grayscaleImage)
		blurredImage = blurredImageObject.blurImage
		blurredImage.save("out/blur-" + name)

		thresholdedImageObject = algorithms.thresholdedImage(blurredImage,0)
		self.thresholdedImage = thresholdedImageObject.thresholdImage
		self.pupilThreshold = thresholdedImageObject.thr
		print "Threshold is %s" % self.pupilThreshold


		self.thresholdedImage.save("out/thresh-" + name)
		#return thresholdedImage


		CannyHoughObject = algorithms.CannyHough(self.thresholdedImage)
		#CannyCircleImage = CannyHoughObject.cvPupil
		self.xPoint = CannyHoughObject.x
		self.yPoint = CannyHoughObject.y
		self.rPoint = CannyHoughObject.r
		#print CannyHoughObject.cvSize
		#print CannyHoughObject.storage
	
		###Test for iris boundary detection###
		thresholded2ImageObject = algorithms.thresholdedImage(blurredImage,self.pupilThreshold+2)
		self.thresholded2Image = thresholded2ImageObject.thresholdImage
		print "Threshold is %s" % thresholded2ImageObject.thr
		self.thresholded2Image.save("out/thresh2-" + name)



