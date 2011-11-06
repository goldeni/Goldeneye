import Image

class HoughTransform:
	def __init__(self,inputImage, rmin, rmax):
		w,h = inputImage.size
		outimg = Image.new('L',(w,h))
		out = outimg.load()

		inp = inputImage.load()

		a_min = int(w/4)
		a_max = w-a_min
		b_min = int(h/4)
		b_max = h-b_min
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
			acci = acc[i]
			for j in range(b):
				acci[j] = [0]*r


		#for p in range(a):
		#	print "P: ",p
		#	for q in range(b):
		#		print "Q: ",q
		#		for s in range(r):
		#			print "S: ",s
		#			accp = acc[p]
		#			accq = accp[q]
		#			accr = accq[r]
		#			print "accp",acc[p]
		#			print "accq",acc[q]
		#			print "accr",acc[r]
		print "Done"

		print "Populating Accumulator..."
		for y in range(h):
		#	print "y: ",y
			for x in range(w):
		#		print "x: ",x
				if inp[x,y] < 128:
					print y,x
					print inp[x,y],"\n"
					for _a in range(a):
						for _b in range(b):
							for _r in range(r):
								s1 = x - (_a + a_min)
								s2 = y - (_b + b_min)
								r1 = _r + r_min
								if (s1 * s1 + s2 * s2 == r1 * r1):
									acca = acc[_a]
									accb = acca[_b]
									accb[_r] += 1
									if accb[_r] >= maxVotes:
										maxVotes = accb[_r]
		print "Done"
		for _a in range(a):
			for _b in range(b):
				for _r in range(r):
					acca = acc[_a]
					accb = acca[_b]
					if accb[_r] >= maxVotes-1:
						total_a += _a + a_min
						total_b += _b + b_min
						total_r += _r + r_min
						amount += 1
		top_a = total_a / amount
		top_b = total_b / amount
		top_r = total_r / amount

		print top_a,top_b,top_r

		self.circle = (top_a,top_b,top_r)

