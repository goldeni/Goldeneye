import Image
import cv
import ImageFilter
import threshold2

class grayscaledImage:
	def __init__(self,inputImage):
		if inputImage.format == 'L':
			self.grayImage = inputImage
		else:
			self.grayImage = self.doGrayscale(inputImage)

	def doGrayscale(self,img):
		return img.convert('L')

class blurredImage:
	def __init__(self,inputImage):
		self.blurRadius = 13
		self.blurImage = inputImage.filter(ImageFilter.MedianFilter(self.blurRadius))

class thresholdedImage:
	def __init__(self,inputImage,flag,pixels):
		if flag == 1:
			self.thresholdImageObject = threshold2.otsuThresholder(inputImage,pixels)
			self.thresholdImage = self.thresholdImageObject.thresholdImage
			#self.thr = threshold2.t
