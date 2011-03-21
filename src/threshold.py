#!/usr/bin/python
import Image, math, sys

# Main thresholding function
def thresh(img):
	o = int(otsu(img))
	lut = [255 if v > int(o) else 0 for v in range(256)] 
	thr = img.point(lut)
	return thr

# Calculates the optimal threshold using Otsu's Method
def otsu(img):
	# Initialize histogram
	hist = img.histogram()

	# Get image size
	dim = img.size
	total = dim[0]*dim[1]

	sum = 0;
	for t in range(255):
		sum += t * hist[t]

	avg = sum/total
	sumB, wB, wF = 0,0,0
	varMax, threshold = 0,0

	for t in range(0,int(avg/2)):
		wB += hist[t]
		if wB == 0:
			continue
		wF = total - wB;
		if wF == 0:
			break

		sumB += t * hist[t]

		mB = sumB / wB
		mF = (sum - sumB) / wF;

		#Calculate Between Class Variance
		varBetween = wB * wF * (mB - mF) * (mB - mF)

		#Check if new maximum found
		if varBetween > varMax:
			varMax = varBetween
			threshold = t
	
	return threshold
