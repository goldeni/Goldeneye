import Image, array, math, time

def quantile(lst, f=0.5):
	l,r = 0,256
	targetCount = int(len(lst)*f)
	while l+1 < r:
		m = (l+r)/2
		count = 0
		for x in lst:
			if x<m: count+=1
		if count <= targetCount:
			l = m
		else:
			r = m
	return l

#def quantile(lst, f=0.5):
#	# build histogram    
#	h = [0] * 256
#	for x in lst:
#		h[x] = h[x]+1

#	# find median value in histogram
#	sum = 0
#	targetSum = int(len(lst)*f)
#	for i in range(0, 255):
#		sum += h[i]
#		if (sum > targetSum):
#			return i


def filter(img):
	src = array.array('B', img.getdata())
	dst = array.array('B', img.getdata())
	w,h=img.size

	r = 3
	mask = []
	for dy in range(-r, r+1):
		dx = int(math.sqrt(r*r-dy*dy))
		for x in range(-dx,dx+1):
			mask += [(x,dy)]

	maskOfs = [x+w*y for x,y in mask]

	pixelsInMask = [0]*len(mask)

#	starttime = time.clock()
	pixelsProcessed = 0

	for y in range(0+r,h-r):
#		elapsed = time.clock()-starttime
#		if elapsed > 0.1 and y % 10 == 0:
#			print "Applying median filter: %3i / %3i: %0.2f %%; %0.1f p/s\r" % (y, h, (y-r)*100.0/(h-r*2), pixelsProcessed/elapsed)
		for x in range(0+r,w-r):
			i = 0

			base = x+y*w
			for ofs in maskOfs:
				pixelsInMask[i] = src[base+ofs]
				i+=1
			dst[x+y*w] = quantile(pixelsInMask, 0.5)
			pixelsProcessed += 1

	imgDest = img.copy()
	imgDest.putdata(dst)
	print
	return imgDest

if __name__ == '__main__':
	main()

def main(img):
	imgDest = filter(img)
#	imgDest.save("../out/filter.bmp")
	return imgDest
