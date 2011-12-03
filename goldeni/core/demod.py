import Image
import math

class unwrap:
        def __init__(self, image, pC, pR, iR):
                self.image = image.load()
                self.pC = pC
                self.pR = pR
                self.iR = iR

        def unwrap(self):
                ang = 256
                w = self.iR - self.pR
                
                polarImg = Image.new("L",(w,ang))
                iRect = polarImg.load()

                for r in range(w):
                        for c in range(ang):
                                curPoint = self.getLoc(c,r)
                                curVal = self.getVal(c,r)

                                iRect[r,c] = curVal
                return polarImg

        def getLoc(self, rtheta, r):
                theta = rtheta * (math.pi / 128)

                r = int(r + self.pR)

                x = int(r * math.cos(theta))
                y = int(r * math.sin(theta))

                x += int(self.pC[0])
                y += int(self.pC[1])

                return x,y

        def getVal(self, theta, r):
                a,b = self.getLoc(theta,r)
                return self.image[a,b]

class demod:
        def __init__(self, image):
                self.image = image
                self.pixelIndex = image.load()

        def demod(self):
                w,h = self.image.size

                bitCode = [0]*2048

                ang = 256
                rad = 1024/ang

                maxFilter = h/3

                bitCodePos = 0

                for aSlice in range(ang):
                        theta = aSlice
                        for rSlice in range(rad):
                                radius = ((rSlice * (h-6)) / (2*rad)) + 3

                                if radius < h-radius:
                                        filterHeight = 2*radius-1
                                else:
                                        filterHeight = 2*(h-radius)-1

                                if filterHeight > w-1:
                                        filterHeight = w-1

                                if filterHeight > maxFilter:
                                        filterHeight = maxFilter
                                
                                pSinObj = sinusoidalFilter(filterHeight,"sine")
                                pCosObj = sinusoidalFilter(filterHeight,"cosine")

                                pSine = pSinObj.generateFilter()
                                pCosine = pCosObj.generateFilter()

                                bitCode[bitCodePos] = self.gaborToPixel(radius,theta,pCosine,self.image,filterHeight)
                                bitCode[bitCodePos+1] = self.gaborToPixel(radius,theta,pSine,self.image,filterHeight)

                                bitCodePos += 2
                return bitCode

        def gaborToPixel(self, rho, phi, sFilter, image,d):
                filterSize = d

                runningTotal = 0.0

                angles = 256

                for i in range(filterSize):
                        for j in range(filterSize):
                                imageY = j + phi - (filterSize/2)

                                imageY %= angles

                                if imageY < 0:
                                        imageY += angles

                                imageX = i + rho - (filterSize/2)

                                a = sFilter[i][j]
                                print "imageX: ",imageX
                                print "imageY: ",imageY
                                print "Value: ",self.pixelIndex[imageX,imageY]

                                runningTotal += sFilter[i][j] * self.pixelIndex[imageX,imageY]

                                if runningTotal >= 0:
                                        return 1
                                else:
                                        return 0




class sinusoidalFilter:
        def __init__(self,d,filterType):
                self.d = d
                self.filterType = filterType

        def generateFilter(self):
                sum = 0

                filterArray = [[0]*self.d]*self.d

                for i in xrange(self.d):
                        phi = i - (self.d/2)
                        if self.filterType == "sine":
                                filterArray[0][i] = self.cosWaveletValue(phi,self.d)
                        elif self.filterType == "cosine":
                                filterArray[0][i] = self.sinWaveletValue(phi,self.d)
                        else:
                                print "Not a valid filter type: something went wrong"
                                sys.exit()
                                        
                        sum += filterArray[0][i]
                for i in xrange(self.d):
                        filterArray[0][i] -= (sum / self.d)
                for i in xrange(1,self.d):
                        for j in xrange(self.d):
                                filterArray[i][j] = filterArray[0][j]

                gausObj = Gaussian(self.d)
                gaussianFilter = gausObj.generateFilter()
#                print "gausFilt: ",gaussianFilter

                newFilt = self.multiplyBy(gaussianFilter,filterArray)
#                print "newFilt: ",newFilt

                filterArray = newFilt

                for i in xrange(self.d):
                        rowSum = 0
                        for j in xrange(self.d):
                                rowSum += filterArray[i][j]

                        for j in xrange(self.d):
                                filterArray[i][j] -= rowSum / float(self.d)
                return filterArray

        def cosWaveletValue(self,phi,d):
                return math.cos(math.pi * phi / (d/2))

        def sinWaveletValue(self,phi,d):
                return math.sin(math.pi * phi / (d/2))

        def multiplyBy(self,filt,otherFilter):
                d = len(filt)
                if d != len(otherFilter):
                        print "Error: Some array problems happened"
                        sys.exit()
                for i in xrange(d):
                        for j in xrange(d):
                                filt[i][j] *= otherFilter[i][j]

                return filt



class Gaussian:
        def __init__(self,d):
                self.d = d
                self.peak = 15.0
                self.alpha = (d-1) * 0.4770322291
                self.beta = self.alpha

        def generateFilter(self):
                filterArray = [[0]*self.d]*self.d
                for i in xrange(self.d):
                        rho = i-(self.d/2)
                        for j in xrange(self.d):
                                phi = j-(self.d/2)
                                filterArray[i][j] = self.waveletValue(rho,phi)

                return filterArray

        def waveletValue(self,rho,phi):
                return self.peak * math.exp(-math.pow(rho,2)/math.pow(self.alpha,2)) * math.exp(-math.pow(phi,2) / math.pow(self.beta,2))


