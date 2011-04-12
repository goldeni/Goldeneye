import Image, math, time, array

# Find the median of the list
# f=0.5 means an f-value of 0.5, i.e. the median
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

# faster experimental median using histogram
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

# Filter function, doesn't process edges
# Very slow, needs to be improved
def filter(img):

	# Initialize image arrays
	src = array.array('B', img.getdata())
	dst = array.array('B', img.getdata())
	w,h=img.size

	# Filter radius
	r = 3

	mask = []

	# Calculate mask values
	for dy in range(-r, r+1):
		dx = int(math.sqrt(r*r-dy*dy))
		for x in range(-dx,dx+1):
			mask += [(x,dy)]

	maskOfs = [x+w*y for x,y in mask]

	pixelsInMask = [0]*len(mask)

	pixelsProcessed = 0

	# Main processing loop.
	# Run through image, add pixels to list, calculate median, and store results in second image array
	for y in range(0+r,h-r):
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
	return imgDest

if __name__ == '__main__':
	main()

def main(img):
	imgDest = filter(img)
	return imgDest
