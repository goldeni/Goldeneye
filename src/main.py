#!/usr/bin/python

import Image,sys,ImageFilter,os,medianfilter, threshold, operators, os

img = Image.open(sys.argv[1])

name = os.path.basename(sys.argv[1])
print name
# Convert image to 8-bit if it isn't
if img.format == 'L': im = img
else: im = img.convert('L')

# Threshold unblurred image
#tm = threshold.thresh(im)

# Use custom median filter (functional, but slow)
#m = medianfilter.main(im)

# use ImageFilter median filter
m = im.filter(ImageFilter.MedianFilter(11))

# Threshold blurred image
t = threshold.thresh(m)

# Save everything
im.save("../out/3-1.jpg")
#tm.save("../out/3-3.jpg")
m.save("../out/3-2.jpg")
t.save("../out/3-4.jpg")

# Apply various edge-detection filters to the image
for i in ['prewitt']:
#, 'sobel', 'roberts', 'scharr']:
	#x = operators.main(im, i)
	#y = operators.main(m, i)
	#z = operators.main(tm, i)
	p = operators.main(t, i)
	#x.save("../out/3-1" + i + ".jpg")
	#y.save("../out/3-2" + i + ".jpg")
	#z.save("../out/3-3" + i + ".jpg")
	p.save("../out/3-4" + i + ".jpg")
