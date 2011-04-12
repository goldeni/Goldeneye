#!/usr/bin/python

import Image,sys,ImageFilter,os,threshold,operators,time,cv

def main(path):


	name = os.path.basename(path)

	print "Process Started on",name
	start = time.time()

	img = Image.open(path)

	# Convert image to 8-bit if it isn't
	if img.format == 'L': im = img
	else: im = img.convert('L')

	# Threshold unblurred image
	#tm = threshold.thresh(im)

	# Use custom median filter (functional, but slow)
	#m = medianfilter.main(im)

	print "Blurring Started"
	filterstart = time.time()

	# use ImageFilter median filter
	m = im.filter(ImageFilter.MedianFilter(11))

	print "Burring Complete: Time = ",time.time()-filterstart,"ms"

	# Threshold blurred image
	t = threshold.thresh(m)

	# Save everything
	im.save("../out/3-1.jpg")
	#tm.save("../out/3-3.jpg")
	m.save("../out/3-2.jpg")
	t.save("../out/3-4.jpg")

	# Apply various edge-detection filters to the image
#	for i in ['roberts']:
	#, 'sobel', 'roberts', 'scharr']:
		#x = operators.main(im, i)
		#y = operators.main(m, i)
		#z = operators.main(tm, i)
#		p = operators.main(t, i)
		#x.save("../out/3-1" + i + ".jpg")
		#y.save("../out/3-2" + i + ".jpg")
		#z.save("../out/3-3" + i + ".jpg")
#		p.save("../out/3-4" + i + ".jpg")

	# convert t to an opencv image, convolve, then convert back and return
	
	convstart = time.time()
	tmp = cv.CreateImageHeader(t.size, cv.IPL_DEPTH_8U, 1)
	cv.SetData(tmp, t.tostring())
	print "Convolution Started"
	cv.Canny(tmp,tmp,0,255,3)
	p = Image.fromstring("L", cv.GetSize(tmp), tmp.tostring())
	print "Convolution Done: Time = ", (time.time()-convstart)*1000
	p.save("../out/test.jpg")

	print "Process Complete: Time = ",(time.time()-start)*1000,"ms"
	print p
	return p	

