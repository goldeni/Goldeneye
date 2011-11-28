import Image

class threshold:
	def __init__(self,hist):
		self.hst = hist

	def pupilThresh(self,minThresh,maxThresh):
		pupilMax = -1
		pupilMaxIndex = -1
		for t in range(minThresh,maxThresh):
			if self.hst[t] > pupilMax:
				pupilMax = self.hst[t]
				pupilMaxIndex = t
		pupilThreshold = pupilMaxIndex + 8
		return pupilThreshold

	def irisThresh(self,minThresh,maxThresh):
		firstMax = -1
		firstMaxIndex = -1
		for t in range(minThresh,maxThresh):
			if self.hst[t] > firstMax:
				firstMax = self.hst[t]
				firstMaxIndex = t
		secondMax = -1
		secondMaxIndex = -1
		for t in range(firstMaxIndex + 20,maxThresh):
			if self.hst[t] > secondMax:
				secondMax = self.hst[t]
				secondMaxIndex = t
		for t in range(minThresh, firstMaxIndex - 20):
			if self.hst[t] > secondMax:
				secondMax = self.hst[t]
				secondMaxIndex = t

		if firstMaxIndex > secondMaxIndex:
			tmp = firstMaxIndex
			firstMaxIndex = secondMaxIndex
			secondMaxIndex = tmp

		tmin = firstMax
		minIndex = -1
		for t in range(firstMaxIndex,secondMaxIndex):
			if self.hst[t] < tmin:
				tmin = self.hst[t];
				minIndex = t
		
		if minIndex > 170 or minIndex <= minThresh+8:
			minIndex = 160

		irisThresh = (firstMaxIndex + secondMaxIndex)/2
#		print "New Threshold: ", firstMaxIndex, secondMaxIndex, minIndex, irisThresh

		return irisThresh 
