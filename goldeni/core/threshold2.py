import Image

class otsuThresholder:
	def __init__(self,inputImage):
		self.t = int(self.otsu(inputImage))

		lut = [255 if v > int(self.t) else 0 for v in range(256)]
		self.thresholdImage = inputImage.point(lut)

	def otsu(self,inputImage):
		hist = inputImage.histogram()

		dim = inputImage.size
		total = dim[0]*dim[1]

		sum = 0
		for t in range(255):
			sum += t * hist[t]

		avg = sum/total

		sumB, wB, wF = 0,0,0
		varMax, threshold = 0,0

		for t in range(0,int(avg/2)):
			wB += hist[t]
			if wB == 0:
				continue
			wF = total - wB
			if wF == 0:
				break

			sumB += t * hist[t]

			mB = sumB/wB
			mF = (sum - sumB)/wF

			varBetween = wB * wF * (mB - mF) * (mB - mF)

			if varBetween > varMax:
				varMax = varBetween
				threshold = t

			return threshold
