import algorithms
import os
import Image
import cv
import hough
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
		##thresholdedImageObject = algorithms.thresholdedImage(blurredImage,0,70)
		##self.thresholdedImage = thresholdedImageObject.thresholdImage
		##self.pupilThreshold = thresholdedImageObject.thr
		##print "Threshold is %s" % self.pupilThreshold

		### New thresholding technique. Abstract to class or function in algorithms
		hist = blurredImage.histogram()
		pupilMax = -1
		pupilMaxIndex = -1
		for t in range(0,70):
			if hist[t] > pupilMax:
				pupilMax = hist[t]
				pupilMaxIndex = t
		pupilThreshold = pupilMaxIndex + 4

		lut = [255 if v > pupilThreshold else 0 for v in range(256)]
	
		self.thresholdedImage = blurredImage.point(lut)
		self.thresholdedImage.save("out/thresh1-" + name)

		#CannyHoughObject = algorithms.CannyHough(self.thresholdedImage,35)
		#self.xPoint = int(CannyHoughObject.x)
		#self.yPoint = int(CannyHoughObject.y)
		#self.rPoint = int(ceil(CannyHoughObject.r))

		###############TESTING NEW HOUGH TRANSFORM######################
		
		################################################################

	
		###Test for iris boundary detection###
		### This is slightly more complicated than the pupil detection
		### What we will do it look for the second peak in the histogram,
		### then search around that threshold for the optimal value
		#####EVENTUALLY MOVE TO ALGORITHMS CLASS
		#####Make threshold class only for otsu eyelid detection
		print "Threshold before is %s" % pupilThreshold
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


		SobelPupilObject = algorithms.sobelFilter(self.thresholdedImage)
		SobelPupilImage = SobelPupilObject.outputImage
		SobelIrisObject = algorithms.sobelFilter(threshold2Image)
		SobelIrisImage = SobelIrisObject.outputImage

		SobelPupilImage.save("out/sobelpupil-" + name)
		SobelIrisImage.save("out/sobeliris-" + name)

		HoughObject = hough.HoughTransform(SobelPupilImage,35,55)
		(xPoint,yPoint,rPoint) = HoughObject.circle

#		CannyHoughObject2 = algorithms.CannyHough(threshold2Image,int(self.rPoint*1.5))
#		self.x2Point = int(CannyHoughObject2.x)
#		self.y2Point = int(CannyHoughObject2.y)
#		self.r2Point = int(ceil(CannyHoughObject2.r))

		#########Testing - Display pupil circle in output image###########
		cv_im = self.pilToCV(SobelPupilImage)
		dst = cv.CreateImage(inputImage.size,cv.IPL_DEPTH_8U,3)
		cv.CvtColor(cv_im,dst,cv.CV_GRAY2RGB)
		cv.Circle(dst,(xPoint,yPoint),rPoint,cv.RGB(255, 0, 0),1,2)
		cv.SaveImage("out/circle-"+name,dst)

		HoughObject2 = hough.HoughTransform(SobelPupilImage,90,170)
		(xPoint,yPoint,rPoint) = HoughObject2.circle
		cv_im2 = self.pilToCV(SobelIrisImage)
		dst2 = cv.CreateImage(inputImage.size,cv.IPL_DEPTH_8U,3)
		cv.CvtColor(cv_im2,dst2,cv.CV_GRAY2RGB)
		cv.Circle(dst2,(xPoint,yPoint),rPoint,cv.RGB(255, 0, 0),1,2)
		cv.SaveImage("out/circle2-"+name,dst2)
		##################################################################
		#########Testing - Display pupil circle in output image###########
		#cv.Circle(dst,(xPoint,yPoint),rPoint,cv.RGB(0, 255, 0),1,2)
		#cv.SaveImage("out/circle2-"+name,dst)

		##################################################################

		

