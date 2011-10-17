#!/usr/bin/python

import algorithms
import os,Image,cv

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

		thresholdedImageObject = algorithms.thresholdedImage(blurredImage,1,1)
		self.thresholdedImage = thresholdedImageObject.thresholdImage


		self.thresholdedImage.save("out/thresh-" + name)
		#return thresholdedImage


		####This is starting to work, but is not yet fully functional.
		CannyHoughObject = algorithms.CannyHough(self.thresholdedImage)
		#CannyCircleImage = CannyHoughObject.cvPupil
		self.xPoint = CannyHoughObject.x
		self.yPoint = CannyHoughObject.y
		self.rPoint = CannyHoughObject.r
		#print CannyHoughObject.cvSize
		#print CannyHoughObject.storage
	




