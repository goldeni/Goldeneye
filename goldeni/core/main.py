#!/usr/bin/python

import algorithms
import os,Image

def main(path):
	name = os.path.basename(path)
	inputImage = Image.open(path)

	grayImageObject = algorithms.grayscaledImage(inputImage)
	grayscaleImage = grayImageObject.grayImage
	grayscaleImage.save("out/gray-" + name)

	blurredImageObject = algorithms.blurredImage(grayscaleImage)
	blurredImage = blurredImageObject.blurImage
	blurredImage.save("out/blur-" + name)

	thresholdedImageObject = algorithms.thresholdedImage(blurredImage,1,1)
	thresholdedImage = thresholdedImageObject.thresholdImage

	#print "Threshold is " + thresholdedImageObject.thr
	thresholdedImage.save("out/thresh-" + name)
	return thresholdedImage

	#CannyHoughObject = algorithms.CannyHough(thresholdedImage)
	#print CannyHoughObject.cvSize
	#print CannyHoughObject.storage
