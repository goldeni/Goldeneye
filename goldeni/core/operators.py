import Image, time


class SobelFilter:

	def __init__(self, inputImage):	
		w, h = inputImage.size
		pixels = inputImage.load()
		print "Convolution Started"
		self.outimg = self.convolve(pixels, w, h)

	def testconvolve(self, pxls, w, h):
		offset = 1
		for imgX in range(w):
			for imgY in range(h):
				values = [0] * 9
				for filterX in range(-offset,offset):
					for filterY in range(-offset,offset):
						print "Pixel [",imgX,"],[",imgY,"]"
						print "Offset[",filterX,"],[",filterY,"]"
						x = imgX+filterX
						y = imgY+filterY
						pixelValue = pxls[x,y]
						print "PixelValue = ",pixelValue
						a = filterX + offset
						b = filterY + offset
						print "A = ",a
						print "B = ",b
						print "A+3B = ",a+3*b
						xmask, ymask = self.get_sobel_masks()
						values[a+3*b] = int(pixelValue * xmask[b,a])
		return values

	# Convolve the kernels with the image to approximate the gradient
	def convolve(self, pixels, width, height):

		# Initialize the various kernels
		dim = 3
		xmask, ymask = self.get_sobel_masks()

		iend = width
		jend = height

		outimg = Image.new('L',(width,height))
		out = outimg.load()

		# Main loop
		# Runs through image and calculates an approximation of the magnitude of the gradient at all points.
		for i in xrange(iend):
			for j in xrange(jend):
				sumX,sumY = 0,0
				mag = 0
				if j == 0 or j == height-1: mag = 0
				elif i == 0 or i == width-1: mag = 0
				else:
					for m in xrange(dim):
						for n in xrange(dim):
							if m>i or n>j: continue
							# Sum x and y gradient-approximations
							pix = pixels[i-m,j-n]
							sumX += xmask[m,n] * pix
							sumY += ymask[m,n] * pix

				# Approximate the magnitude of the gradient
				mag = (abs(sumX)+abs(sumY))/(dim*dim)
				
				# Normalize bad results
				if mag > 255: mag = 255
				elif mag < 0: mag = 0

				# Output gradient approximation to an image array
				out[i,j] = 255 - mag
		return outimg

	def get_sobel_masks(self):
		xmask = {}
		ymask = {}

		xmask[(0,0)] = -1
		xmask[(0,1)] = 0
		xmask[(0,2)] = 1
		xmask[(1,0)] = -2
		xmask[(1,1)] = 0
		xmask[(1,2)] = 2
		xmask[(2,0)] = -1
		xmask[(2,1)] = 0
		xmask[(2,2)] = 1

		
		ymask[(0,0)] = 1
		ymask[(0,1)] = 2
		ymask[(0,2)] = 1
		ymask[(1,0)] = 0
		ymask[(1,1)] = 0
		ymask[(1,2)] = 0
		ymask[(2,0)] = -1
		ymask[(2,1)] = -2
		ymask[(2,2)] = -1

		return (xmask, ymask)

	# Old convolve functction
	#def convolve(pixels, width, height, k):
	#	dim = 2
	#	if k == 'scharr':
	#		xmask, ymask = get_scharr_masks()
	#	if k == 'prewitt':
	#		xmask, ymask = get_prewitt_masks()
	#	if k == 'sobel':
	#		xmask, ymask = get_sobel_masks()
	#	if k == 'roberts':
	#		xmask, ymask = get_roberts_masks()
	#		dim = 1
	#
	#	outimg = Image.new('L', (width, height))
	#	outpixels = list(outimg.getdata())
	#
	#	for y in xrange(height):
	#		for x in xrange(width):
	#			sumX, sumY, magnitude = 0,0,0
	#
	#			if y == 0 or y == height-1: magnitude = 0
	#			elif x == 0 or x == width-1: magnitude = 0
	#			else:
	#				for i in xrange(-1,dim):
	#					for j in xrange(-1,dim):
	#						sumX += (pixels[x+i+(y+j)*width]) * xmask[i+1, j+1]
	#						sumY += (pixels[x+i+(y+j)*width]) * ymask[i+1, j+1]
	#
	#			magnitude = abs(sumX) + abs(sumY)
	#
	#			if magnitude > 255: magnitude = 255
	#			if magnitude < 0: magnitude = 0
	#
	#			outpixels[x+y*width] = 255 - magnitude
	#	outimg.putdata(outpixels)
	#	return outimg

