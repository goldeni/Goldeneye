"""
A home for algoriths too complex for the main file, but not complex enough to have their own file
"""

import Image
#import cv
import ImageFilter
import sobelfilter
#import threshold

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
	def __init__(self,inputImage,blur):
		"""
		Uses ImageFilter's MedianFilter functions to blur the image.
		"""
		self.blurImage = inputImage.filter(ImageFilter.MedianFilter(blur))

class sobelFilter:
	def __init__(self, inputImage):
		SobelObject = sobelfilter.SobelFilter(inputImage)
		self.outputImage = SobelObject.outimg

