import Image
import cv
import ImageFilter
import threshold

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
		self.blurRadius = 9
		self.blurImage = inputImage.filter(ImageFilter.MedianFilter(self.blurRadius))

# Will probably not need pixel objects. Just ignore thresholds <= the first Otsu result
class thresholdedImage:
	def __init__(self,inputImage,flag,pixels):
		if flag == 1:
			self.thresholdImageObject = threshold.otsuThresholder(inputImage,pixels)
			self.thresholdImage = self.thresholdImageObject.thresholdImage
			#self.thr = threshold.t

# Starting to behave, should be running soon
class CannyHough:
	def __init__(self, inputImage):
		cvImage = cv.CreateImageHeader(inputImage.size, cv.IPL_DEPTH_8U, 1)
		cv.SetData(cvImage, inputImage.tostring())
		self.cvSize = cv.GetSize(cvImage)

		cv.SaveImage("out/xyz.jpg",cvImage)

		self.storage = cv.CreateMat(50, 1, cv.CV_32FC3)

		#Fix this stuff
		circles = cv.HoughCircles(cvImage,self.storage,cv.CV_HOUGH_GRADIENT,3,25,200,100,25,60);

		(self.x,self.y,self.r) = self.storage[0,0]
