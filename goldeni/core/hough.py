import Image
from math import sqrt,ceil

class HoughTransform:
	def __init__(self,inputImage, topLeft, widthHeight, rmin, rmax):
		self.inputImage = inputImage
		self.topLeft = topLeft
		self.widthHeight = widthHeight
		self.rmin = rmin
		self.rmax = rmax

	def pupilHough(self):
		w,h = self.inputImage.size
		outimg = Image.new('L',(w,h))
		out = outimg.load()
		inp = self.inputImage.load()

		a_min, b_min = self.topLeft
		a_max, b_max = [sum(i) for i in zip(self.topLeft,self.widthHeight)] 
		r_min = self.rmin
		r_max = self.rmax

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
                return top_a,top_b,top_r

        '''This function is so bad, it should be illegal.
           There's no excuse for this hack other than to
           save a large amount of time in iris-detection.'''
        def irisHough(self,pX,pY,rmin):
		w,h = self.inputImage.size
		outimg = Image.new('L',(w,h))
		out = outimg.load()
		inp = self.inputImage.load()

                a = w-pX
                b = h-pY

                if pX > a:
                        if a>b:
                                if b>pY:
                                        sd=pY
                                else:
                                        sd=b
                        else: sd=a
                else:
                        sd = pX

                maxVotes = -1
                maxVotesR = -1
                circ=[]
                for x in range(-2,3):
                        for y in range(-2,3):
                                if sd-6>rmin+10:
                                        print "WTF? Pupil detection probably failed, idk.",sd,rmin
                                for r in range(rmin+10,125):
                                        cList = []
                                        votes = 0
                                        for xV in range(pX-rmin,pX+rmin+1):
                                                p2 = (xV-(pX+x))*(xV-(pX+x))
                                                r2 = r*r
                                                if r2 < p2:
                                                        continue
                                                posY = sqrt(r2 - p2)+(pY+y)
                                                negY = -sqrt(r2 - p2)+(pY+y)
                                                cList.append((int(xV),int(posY)))
                                                cList.append((int(xV),int(negY)))
                                        for i in cList:
                                                #print i,inp[i[0],i[1]]
                                                if inp[i[0],i[1]] != 255:
                                                       votes += (255-(inp[i[0],i[1]]))
                                                       #votes += 1
                                        if votes >= maxVotes:
                                                print "\n\nNew Max: ", votes, r
                                                maxVotes = votes
                                                maxVotesR = r
                                        circ.append(maxVotesR)
                                        print "\n",r,votes 
                                        del votes
                return max(circ) 
