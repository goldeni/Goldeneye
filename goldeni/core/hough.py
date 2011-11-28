import Image
import sys #tmp
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

		#print "Initializing Accumulator..."

		acc = [0]*a
		for i in range(a):
			acc[i] = [0]*b
			for j in range(b):
				acc[i][j] = [0]*r

		#print "Done"

		#print "Populating Accumulator..."
		for x in range(10,w-10,2):
			for y in range(10,h-10,2):
				if inp[x,y] == 0:
					for _a in range(a):
						for _b in range(b):
							for _r in range(r/2,r):
								s1 = x - (_a + a_min)
								s2 = y - (_b + b_min)
								#r1 = _r + ra
								if (s1 * s1 + s2 * s2 == _r * _r):
									new = acc[_a][_b][_r]
									if new >= maxVotes:
										maxVotes = new
		#print "Done"
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

		#print "Tops: ",top_a,top_b,top_r
		del acc
		self.circle0 = top_a + top_r, top_b
		self.circle1 = top_a - top_r, top_b
		self.circle2 = top_a, top_b + top_r
                return top_a,top_b,top_r

        '''This function is so bad, it should be illegal. There's no excuse for 
           this hack other than to save a large amount of time in iris-detection.
	   It essentially populates a list of the points on a circle of radius r,
           then checks how many black points lie on the circle. It then chooses 
           the circle withe the most votes.'''
        def irisHough(self,pX,pY,rmin):
		w,h = self.inputImage.size
		outimg = Image.new('L',(w,h))
		out = outimg.load()
		inp = self.inputImage.load()

                a = w-pX
                b = h-pY

		sd = min(a,b,pX,pY) - 5


                maxVotes = -1
                maxVotesR = -1
                circ=[]
                for xC in range(-2,3):
                        for yC in range(-2,3):
                                #if sd-6>rmin+10:
                                        #print "WTF? Pupil detection probably failed, idk.",sd,rmin
                                for r in range(rmin+10,sd):
                                        cList = []
                                        votes = 0
                                        # Populating the list of circular points
                                        # Circles are hard, so we need to use a clever algorithm
                                        #  to generate the list. Specifically, we use
                                        #   http://en.wikipedia.org/wiki/Midpoint_circle_algorithm
#                                        for xV in range(pX-rmin,pX+rmin+1):
#                                                p2 = (xV-(pX+xC))*(xV-(pX+xC))
#                                                r2 = r*r
#                                                if r2 < p2:
#                                                        continue
#                                                posY = sqrt(r2 - p2)+(pY+yC)
#                                                negY = -sqrt(r2 - p2)+(pY+yC)
#                                                cList.append((int(xV),int(posY)))
#                                                cList.append((int(xV),int(negY)))

                                        ############################################
                                        f =  1-r
                                        ddF_x = 1
                                        ddF_y = -2 * r
                                        x = 0
                                        y = r

                                        xx = pX + xC
                                        yy = pY + yC

                                        cList.append((xx, yy+r))
                                        cList.append((xx, yy-r))
                                        cList.append((xx+r, yy))
                                        cList.append((xx-r, yy))

                                        while x < y:
                                                if f >= 0:
                                                        y -= 1
                                                        ddF_y += 2
                                                        f+= ddF_y
                                                x+=1
                                                ddF_x += 2
                                                f += ddF_x

                                                cList.append((xx+x, yy+y))
                                                cList.append((xx-x, yy+y))
                                                cList.append((xx+x, yy-y))
                                                cList.append((xx-x, yy-y))
                                                cList.append((xx+y, yy+x))
                                                cList.append((xx-y, yy+x))
                                                cList.append((xx+y, yy-x))
                                                cList.append((xx-y, yy-x))
                                        ############################################
                                        for i in cList:
                                                #print i,inp[i[0],i[1]]
                                                if inp[i[0],i[1]] != 255:
                                                       votes += (255-(inp[i[0],i[1]]))
                                                       #votes += 1
                                        if votes >= maxVotes:
                #                                print "\n\nNew Max: ", votes, r
                                                maxVotes = votes
                                                maxVotesR = r
                                        circ.append(maxVotesR)
                 #                       print "\n",r,votes 
                                        del votes
                return maxVotesR 
