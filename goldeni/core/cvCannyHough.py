import cv

class CannyHough:
	def __init__(self, inputImage):
		CvSeq* self.circles = cvHoughCircles( inputImage, storage, CV_HOUGH_GRADIENT, 2, gray->height/4, 200, 100 );
		print self.circles
