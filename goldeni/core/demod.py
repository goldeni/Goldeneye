import Image
import math

''' Unwraps an image using a polar coordinate system
    pC - A two-element list containing the pupil center (x,y)
    pR - The pupil radius
    iR - The iris radius
'''
class unwrap:
        def __init__(self, image, pC, pR, iR):
                self.image = image.load()
                self.pC = pC
                self.pR = pR
                self.iR = iR

        # Performs the unwrapping. Returns the rectangular representation of the iris.
        def unwrap(self):
                # Number of angles. Specifies the width of the image.
                ang = 256
                # Difference in radii = height of image
                w = self.iR - self.pR
                
                # Create blank image with specified dimensions.
                polarImg = Image.new("L",(ang,w))
                # Create pixel access object
                iRect = polarImg.load()

                # Main loop - runs through all angles and radii
                for r in range(w):
                        for c in range(ang):
                                # Get x,y of current point (not needed any more)
                                curPoint = self.getLoc(c,r)
                                # Get value of that point
                                curVal = self.getVal(c,r)

                                # Set
                                iRect[c,r] = curVal
                return polarImg

        # Get x,y of a polar point
        def getLoc(self, rtheta, r):
                # Convert to radians
                theta = rtheta * (math.pi / 128)

                r = r + self.pR

                # Get x,y and offset by pupil center
                x = int(r * math.cos(theta))
                y = int(r * math.sin(theta))
                x += int(self.pC[0])
                y += int(self.pC[1])

                return x,y
        
        # Get value of image at a point.
        def getVal(self, theta, r):
                a,b = self.getLoc(theta,r)
                return self.image[a,b]

''' Demodulate the polar image into an irisCode
    image - the polar image
'''
class demod:
        def __init__(self, image):
                self.image = image
                self.pixelIndex = image.load()
                self.w,self.h = self.image.size

        # Do the demodulation
        def demod(self):
                # Initialize empty irisCode
                bitCode = [0]*2048

                # Number of angular and radial divisions.
                # ang * rad should be half the iriscode length you want.
                ang = 256
                rad = 1024/ang

                # We don't want gigantic filters, so we limit to h/3
                maxFilter = int(self.h/3)

                # Initial bitcode position
                bitCodePos = 0

                # Main loop
                # Runs through all angles and radii
                for aSlice in range(ang):
                        theta = aSlice
                        for rSlice in range(rad):
                                # Equally space radii, but start at 3 to avoid small filters.
                                radius = int(((rSlice * (self.h-6)) / (2*rad)) + 3)

                                # Set the filterheight depending on what
                                # side of the image it is on.
                                if radius < self.h-radius:
                                        filterHeight = 2*radius-1
                                else:
                                        filterHeight = 2*(self.h-radius)-1

                                # The max filterheight should clearly be less than w
                                if filterHeight > self.w-1:
                                        filterHeight = self.w-1

                                # Same as above.
                                if filterHeight > maxFilter:
                                        filterHeight = maxFilter
                                
                                # Create cosine and sine filters.
                                pSinObj = sinusoidalFilter(filterHeight,"sine")
                                pCosObj = sinusoidalFilter(filterHeight,"cosine")

                                pSine = pSinObj.generateFilter()
                                pCosine = pCosObj.generateFilter()

                                # Calculate bitcodes and add to the irisCode list.
                                bitCode[bitCodePos] = self.gaborToPixel(radius,theta,pCosine,self.image,filterHeight)
                                bitCode[bitCodePos+1] = self.gaborToPixel(radius,theta,pSine,self.image,filterHeight)

                                bitCodePos += 2
                return bitCode

        def gaborToPixel(self, rho, phi, sFilter, image,d):
                filterSize = len(sFilter)

                # Used for convolution
                runningTotal = 0.0

                angles = self.w

                # Convolve the filter with the image to obtain phasor
                for i in range(filterSize):
                        for j in range(filterSize):
                                # Calculate what pixel to process
                                imageY = j + phi - (filterSize/2)

                                imageY %= angles

                                # This shouldn't happen, but whatever.
                                if imageY < 0:
                                        imageY += angles

                                # Calculate what pixel to process
                                imageX = i + rho - (filterSize/2)

                                # Add pixel convolution to runningtotal
                                try:
                                        runningTotal += sFilter[i][j] * self.pixelIndex[imageY,imageX]
                                except IndexError:
                                        pass
                                        print "Index Error"
                                        print "i,j",i,j
                                        print "imageX: ",imageX
                                        print "imageY: ",imageY
                                        print sFilter[i][j]
                                        print "Value: ",self.pixelIndex[imageY,imageX],"\n"

                # If the imaginary part of the demodulation phasor is positive...
                if runningTotal >= 0:
                        return 1
                else:
                        return 0



'''Generate a sine or cosine filter
   d - dimension
   filterType - "sine" or "cosine"
'''
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


