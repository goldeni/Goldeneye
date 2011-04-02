#!/usr/bin/python
import Image, time

# Main thresholding function
def thresh(img):
	print "Thresholding started"
	start = time.time()
	o = int(otsu(img))
	lut = [255 if v > int(o) else 0 for v in range(256)] 
	thr = img.point(lut)
	print "Thresholding done: time =", (time.time()-start)*1000, "ms"
	print "Threshold:",o
	return thr

# Calculates the optimal threshold using Otsu's Method
def otsu(img):
	# Initialize histogram
	hist = img.histogram()

	# Get image size
	dim = img.size
	total = dim[0]*dim[1]

	# Get sum for averaging the intensity
	sum = 0;
	for t in range(255):
		sum += t * hist[t]

	avg = sum/total

	# Initialize variables
	sumB, wB, wF = 0,0,0
	varMax, threshold = 0,0

	# Main loop (the entire process thresholds three time. we'll eventually add variables based on which thrershold it is)
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

		# Calculate between-class variance
		varBetween = wB * wF * (mB - mF) * (mB - mF)

		# Find maximum between-class variance
		if varBetween > varMax:
			varMax = varBetween
			threshold = t
	
	return threshold
