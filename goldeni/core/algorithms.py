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
		self.blurRadius = 13
		self.blurImage = inputImage.filter(ImageFilter.MedianFilter(self.blurRadius))

class thresholdedImage:
	def __init__(self,inputImage,flag,pixels):
		if flag == 1:
			self.thresholdImageObject = threshold.otsuThresholder(inputImage,pixels)
			self.thresholdImage = self.thresholdImageObject.thresholdImage
			#self.thr = threshold.t

class CannyHough:
	def __init__(self, inputImage):
		cvImage = cv.CreateImageHeader(inputImage.size, cv.IPL_DEPTH_8U, 1)
		cv.SetData(cvImage, inputImage.tostring())
		self.cvSize = cv.GetSize(cvImage)

		cv.SaveImage("out/xyz.jpg",cvImage)

		self.storage = cv.CreateMat(50, 1, cv.CV_32FC3)

		#Fix this shit
		circles = cv.HoughCircles(cvImage,self.storage,cv.CV_HOUGH_GRADIENT,2,(self.cvSize[0])/4,100,50,0,200);

		for (x, y, radius) in circles:
			print x + "\n"
			print y + "\n"
			print radius + "\n"
