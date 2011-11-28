#!/usr/bin/python

#libraries
import Image
import sys
import glob
import time
import matplotlib.pyplot as plt

#modules
import algorithms
import threshold 
import os
import hough
import imgUtils
import demod

class main:
	def __init__(self,path):
		# Start timing  
		initTime = time.time()

		# Get the image name
		name = os.path.basename(path)

                # Windows is dumb and creates a Thumbs.db file for each directory with an image.
                # When doing batch processing, its a good idea to ignore this file.
                if name == "Thumbs.db":
                        sys.exit()

		print "Processing File: ",name

		# Open image
		inputImage = Image.open(path)

		w,h = inputImage.size
                print "Size: ",w,h

		# If image is not 8-bit, grayscale it
		preGS = time.time()
		grayImageObject = algorithms.grayscaledImage(inputImage)
		grayscaleImage = grayImageObject.grayImage
		GStime = time.time() - preGS
		print "It took %.3f" % (1000 * GStime),"ms\n"

		# Blur the image for pupil detection
                print "Blurring for pupil detection"
		preB = time.time()
		blurredImageObject = algorithms.blurredImage(grayscaleImage,11)
		blurredImage = blurredImageObject.blurImage
		Btime = time.time() - preB
		print "Blurring Done"
		print "It took %.3f" % (1000 * Btime),"ms\n"

		prePT = time.time()
		hist = blurredImage.histogram()
		ind = range(256)
		threshObj = threshold.threshold(hist)
		pupilThreshold = threshObj.pupilThresh(0,70)
		lut = [255 if v > pupilThreshold else 0 for v in range(256)]
	
		pupilThreshImage = blurredImage.point(lut)
		PTtime = time.time() - prePT
		print "Threshold 1 saved"
		print "It took %.3f" % (1000 * PTtime),"ms\n"

		preB2 = time.time()
		iBlurredImageObject = algorithms.blurredImage(grayscaleImage,3)
		iBlurredImage = blurredImageObject.blurImage
		B2time = time.time() - preB2
		print "Blurring pt 2 Done"
		print "It took %.3f" % (1000 * B2time),"ms\n"

		print "Threshold before is %s" % pupilThreshold
		irisThresh = threshObj.irisThresh(pupilThreshold,240)

		lut = [255 if v > irisThresh else 0 for v in range(256)]

		irisThreshImage = iBlurredImage.point(lut)
		print "Threshold 2 saved"

                preSP = time.time()
		SobelPupilObject = algorithms.sobelFilter(pupilThreshImage)
		SobelPupilImage = SobelPupilObject.outputImage
		SPtime = time.time() - preSP
		print "Threshold 1 saved"
		print "It took %.3f" % (1000 * SPtime),"ms\n"


                ##################################################
                ###########Pre-hough pupil-processing.############
                #Looks for clusters of black to estimate the
                #pupil size and location. This is a quick hack and
                #does not work in all cases, such as an image with
                #a lot of areas as dark as the pupil##############
                ##################################################
		prePH = time.time()
		pupilPixels = pupilThreshImage.load()
		print "Testing threshold and determining bounding box for pupil..."
		sumx = 0
		sumy = 0
		amount = 0

		for x in range(10,w):
			for y in range(10,h):
				if pupilPixels[x,y] == 0:
					sumx += x
					sumy += y
					amount += 1

		if sumx == 0 or sumy == 0:
			print "Sorry brah, the pupil's gone"
			sys.exit()

		sumx /= amount
		sumy /= amount

		pupilBoxCenter = (sumx, sumy)
                
                # sumx is the average x-location of the black pixels
                # sumy is the average y-location of the black pixels
                # A good idea would to have radii calculated for 4
                # directions, left and right, x and y, then average
		radius = sumx
		print "Initial radius: ",radius
		while pupilPixels[radius,sumy] == 0:
			radius += 1
		radius -= sumx - 2

		print "Final radius = ",radius

		print "Done"
		HoughObject = hough.HoughTransform(SobelPupilImage,(sumx-1,sumy-1),(4,4),radius-4,radius+4)
		pX,pY,pR = HoughObject.pupilHough()

		PHtime = time.time() - prePH
		print "Pupil Circle Fit Done"
		print "It took %.3f" % (1000 * PHtime),"ms\n"


		preSI = time.time() 
		SobelIrisObject = algorithms.sobelFilter(irisThreshImage)
		SobelIrisImage = SobelIrisObject.outputImage
		SItime = time.time() - preSI
		print "Threshold 1 saved"
		print "It took %.3f" % (1000 * SItime),"ms\n"

                preIH = time.time()
                irisHoughObj = hough.HoughTransform(SobelIrisImage,(0,0),(0,0),0,0)
                iR = irisHoughObj.irisHough(pX,pY,pR)
                IHtime = time.time() - preIH
                print "Iris detected"
                print "It took %.3f" % (1000 * IHtime),"ms\n"


                totalTime = time.time()-initTime
		print "Segmentation Done"
                print "It took %.3f" % (1000 * totalTime),"ms\n"

                print "Unwrapping"
                unwrapObj = demod.unwrap(inputImage,(pX,pY),pR,iR)
                polarImg = unwrapObj.unwrap()
                polarImg.save("out/polar-" + name)
                print "Unwrapping done and saved"

                print "Demodulating"
                #irisCode = unwrapObj.demod(polarImg)


		# Save various images.
                # Mainly used to debug in case of a failure.
                # This will be set in the prefences.
                self.saveImagePref = 0
                if (self.saveImagePref == 1):
	        	grayscaleImage.save("out/gray-" + name)
		        blurredImage.save("out/blur-" + name)
        		pupilThreshImage.save("out/thresh1-" + name)
        		irisThreshImage.save("out/thresh2-" + name)
        		SobelPupilImage.save("out/sobelpupil-"+name)
        		SobelIrisImage.save("out/sobeliris-"+name)

                self.saveHist = 0
                if (self.saveHist == 1):
        		plt.bar(ind,hist,color='b')
        		plt.savefig("out/hist-" + name + ".png")

		# Draw circles on result image
		pupilDrawObject = imgUtils.Utils(inputImage)
		pupilDraw = pupilDrawObject.drawCircle(pX,pY,pR)
		irisDrawObject = imgUtils.Utils(inputImage)
		irisDraw = irisDrawObject.drawCircle(pX,pY,iR)
		inputImage.save("out/iriscircle1-" + name)


if __name__ == "__main__":
	argc = len(sys.argv)
	for i in range(1,argc):
		main(sys.argv[i])

