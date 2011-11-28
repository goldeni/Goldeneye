import Image, time


class SobelFilter:

	def __init__(self, inputImage):
		w, h = inputImage.size
		pixels = inputImage.load()
#		print "Convolution Started"
		self.outimg = self.convolve(pixels, w, h)

	# Convolve the kernels with the image to approximate the gradient
	def convolve(self, pixels, width, height):

		# Initialize the various kernels
		dim = 3
		xmask, ymask = self.get_sobel_masks()

		outimg = Image.new('L',(width,height))
		out = outimg.load()

		# Main loop
		for i in xrange(width):
			for j in xrange(height):
				sumX,sumY = 0,0
				mag = 0
				if j <= 3 or j >= height-4: mag = 0
				elif i <= 3 or i >= width-4: mag = 0
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
				if mag > 96: mag = 255
				else: mag = 0
				#if mag > 255: mag = 255
				#elif mag < 0: mag = 0

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
