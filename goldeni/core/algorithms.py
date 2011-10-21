"""
A set of algorithms that perform the iris segmentation.
"""

import Image
import cv
import ImageFilter
import threshold

class grayscaledImage:
	def __init__(self,inputImage):
		"""
		Test is image is 8-bit grayscale. If not, send it to doGrayscale
		"""
		if inputImage.format == 'L':
			self.grayImage = inputImage
		else:
			self.grayImage = self.doGrayscale(inputImage)

	def doGrayscale(self,img):
		"""
		Perform the grayscaling process. Returns a PIL image.
		"""
		return img.convert('L')

class blurredImage:
	#Implement flag structure to reprocess is blur isn't enough.
	#Make blur dependent on size of image and flag. Develop function to calculate.
	def __init__(self,inputImage):
		"""
		Uses ImageFilter's MedianFilter functions to blur the image.
		"""
		self.blurRadius = 9
		self.blurImage = inputImage.filter(ImageFilter.MedianFilter(self.blurRadius))


class thresholdedImage:
	# Will probably not need pixel objects. Just ignore thresholds <= the first Otsu result.
	# Fix variable names.
	def __init__(self,inputImage,controlThreshold):
		"""
		Constructor for thresholdedImage. Performs Otsu thresholding.
		"""
		self.thresholdImageObject = threshold.otsuThresholder(inputImage, controlThreshold)
		self.thresholdImage = self.thresholdImageObject.thresholdImage
		self.thr = self.thresholdImageObject.t

class CannyHough:
	# Write functions to intelligently tweak parameters. Create flag network to notify this function.
	# Throw exceptions for undetected circles
	def __init__(self, inputImage):
		"""
		Perform Canny edge detection, then a circular Hough transform
		to detect pupil and iris boudaries.
		"""
		cvImage = cv.CreateImageHeader(inputImage.size, cv.IPL_DEPTH_8U, 1)
		cv.SetData(cvImage, inputImage.tostring())
		self.cvSize = cv.GetSize(cvImage)

		cv.SaveImage("out/xyz.jpg",cvImage)

		self.storage = cv.CreateMat(50, 1, cv.CV_32FC3)

		#Fix this stuff
		circles = cv.HoughCircles(cvImage,self.storage,cv.CV_HOUGH_GRADIENT,3,25,200,100,25,60);

		(self.x,self.y,self.r) = self.storage[0,0]
