#!/usr/bin/python
import cv,sys
for arg in sys.argv[1:]:
	im = cv.LoadImageM(str(arg))
	dst = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_16S, 3)
	laplace = cv.Laplace(im, dst)
	cv.SaveImage("results/laplacian-%s" % arg, dst)
