import Image

####Alter threshold to function as projectiris '/processing/processiris.cpp' lines 660+
####and /processing/eimage.cpp lines 101+

class otsuThresholder:
	def __init__(self, inputImage, tmin, tmax):
		self.tmin = tmin
		self.tmax = tmax
		self.t = int(self.otsu(inputImage))
		#Apply the threshold
		lut = [255 if v > int(self.t) else 0 for v in range(256)]
	
		self.thresholdImage = inputImage.point(lut)

	def otsu(self, inputImage):
		hist = inputImage.histogram()
		#print hist[cThresh-2:cThresh+9]

		#dim = inputImage.size
		#total = dim[0]*dim[1]

		#sum = 0
		#for t in range(255):
		#	sum += t * hist[t]

		#avg = sum/total

		#sumB, wB, wF = 0,0,0
		#varMax, threshold = 0,0

		#####Test######
		pupilMax = -1
		pupilMaxIndex = -1
		###############

		for t in range(self.tmin,self.tmax):
			##########Test##########
			if hist[t] > pupilMax:
				pupilMax = hist[t]
				pupilMaxIndex = t
			########################
#			wB += hist[t]
#			if wB == 0:
#				continue
#			wF = total - wB
#			if wF == 0:
#				break
#
#			sumB += t * hist[t]
#
#			mB = sumB/wB
#			mF = (sum - sumB)/wF
#
#			varBetween = wB * wF * (mB - mF) * (mB - mF)
#
#			if varBetween > varMax:
#				varMax = varBetween
#				threshold = t
#
#			return threshold
		return pupilMaxIndex + 4
