import Image
from math import sqrt

class HoughTransform:
	def __init__(self,inputImage, topLeft, widthHeight, rmin, rmax):
		w,h = inputImage.size
		outimg = Image.new('L',(w,h))
		out = outimg.load()

		inp = inputImage.load()

		a_min, b_min = topLeft
		a_max, b_max = [sum(i) for i in zip(topLeft,widthHeight)] 
		r_min = rmin
		r_max = rmax

		a = a_max - a_min
		b = b_max - b_min
		r = r_max - r_min

		top_r = 0
		top_a = 0
		top_b = 0

		total_r = 0
		total_a = 0
		total_b = 0

		amount = 0

		maxVotes = 0

		print "Initializing Accumulator..."

		acc = [0]*a
		for i in range(a):
			acc[i] = [0]*b
			for j in range(b):
				acc[i][j] = [0]*r

		print "Done"

		print "Populating Accumulator..."
		for x in range(10,w-10,2):
			for y in range(10,h-10,2):
				if inp[x,y] == 0:
					for _a in range(a):
						for _b in range(b):
							for _r in range(r):
								s1 = x - (_a + a_min)
								s2 = y - (_b + b_min)
								#r1 = _r + ra
								if (s1 * s1 + s2 * s2 == _r * _r):
									new = acc[_a][_b][_r]
									if new >= maxVotes:
										maxVotes = new
		print "Done"
		for _a in range(a):
			for _b in range(b):
				for _r in range(r):
					if acc[_a][_b][_r] >= maxVotes-1:
						total_a += _a + a_min
						total_b += _b + b_min
						total_r += _r + r_min
						amount += 1
		top_a = total_a / amount
		top_b = total_b / amount
		top_r = total_r / amount

		self.topx = top_a
		self.topy = top_b
		self.topr = top_r

		print "Tops: ",top_a,top_b,top_r
		del acc
		self.circle0 = top_a + top_r, top_b
		self.circle1 = top_a - top_r, top_b
		self.circle2 = top_a, top_b + top_r

