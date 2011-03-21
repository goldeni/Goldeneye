#!/usr/bin/python

import Image,sys,ImageFilter,os,medianfilter, threshold, operators

im = Image.open(sys.argv[1]).convert('L')
tm = threshold.thresh(im)
m = medianfilter.main(im)
t = threshold.thresh(m)
im.save("../out/3-1.jpg")
tm.save("../out/3-3.jpg")
m.save("../out/3-2.jpg")
t.save("../out/3-4.jpg")

for i in ['prewitt', 'sobel', 'roberts', 'scharr']:
	x = operators.main(im, i)
	y = operators.main(m, i)
	z = operators.main(tm, i)
	p = operators.main(t, i)
	x.save("../out/3-1" + i + ".jpg")
	y.save("../out/3-2" + i + ".jpg")
	z.save("../out/3-3" + i + ".jpg")
	p.save("../out/3-4" + i + ".jpg")
