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

        def demod(self):
                w,h = self.image.size()

                ang = 256
                rad = 1024/ang

                maxFilter = h/3

                bitCodePos = 0

                pSine = sineWavelet()
                pCosine = cosinWavelet()

                for aSlice in range(ang):
                        theta = aSlice
                        for rSlice in range(rad):
                                radius = ((rSlice * (h-6)) / (2*rad)) + 3

                                if radius < h-radius:
                                        filterHeight = 2*radius-1
                                else:
                                        filterHeight = 2*(h-radius)-1

                                if filterHeight > maxFilter:
                                        filterHeight = maxFilter

                                #generate filters

                                bitCode[bitCodePos] = gaborToPixel(r,theta,pCosine,rawImage)
                                bitCode[bitCodePos+1] = gaborToPixel(r,theta,pSine,rawImage)

                                bitCodePos += 2

        def gaborToPixel(self, rho, phi, sFilter, d):
                filterSize = d

                runningTotal = 0

                angles = self.image.size[1]

                for i in range(filterSize):
                        for j in range(filterSize):
                                imageY = j+ phi - (filterSize/2)

                                imageY %= n

                                if imageY < 0:
                                        imageY += angles

                                imageX = i + rho - (filterSize/2)

                                runningTotal += sFilter #get filter for (i,j)
                                  #* pixelIndex(imageY,imageX)

                                if runningTotal >= 0:
                                        return 1
                                else:
                                        return 0

        def genFilter(self):
                sum = 0
                for j in range(d):
                        phi = j - (d/2)
                        filterArray[0,j] = waveletValue(phi, d)
                        sum += filterArray[0,j]

                for j in range(d):
                        filterArray -= (sum/d)

                for i in range(1,d):
                        for j in range(d):
                                filterArray[i,j] = filterArray[0,j]

                GaussianObj = Gaussian(d)
                GaussianFilter = GaussianObj.genFilter()
                multiplyBy(GaussianFilter)

                for i in range(d):
                        rowSum = 0

                        for j in range(d):
                                rowSum += filterArray[i,j]

                        for j in range(d):
                                filterArray[i,j] -= rowSum / d



class Gaussian:
        def __init__(self,d):
                self.d = d
                self.peak = peak

                alpha = (d-1)
        def outputPixel(self);
                sum = 0
                pixelValue = 0

                for i,e in enumerate(
        def getFilter(self):
                # Discrete approximation of Gaussian kernel with sigma 1.4
                return [[2,4 ,5 ,4 ,2],
                        [4,9 ,12,9 ,4],
                        [5,12,15,12,5],
                        [4,9 ,12,9 ,4],
                        [2,4 ,5 ,4 ,2]]
        
        def addValue(self,x,y,pixelValue,d):
                values[x + y*d] = int(pixelValue * self.getFilter[y][x])
