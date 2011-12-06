#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np

print sys.stdin
r = 4

def compare(a,b):
        a = a[1:-2].split(',')
        b = b[1:-2].split(',')
        return reduce(lambda x,y:x+y,[int(a[i])^int(b[i]) for i in xrange(len(a))])/float(len(a))

f = [i for i in sys.stdin]
lst = [compare(f[i],f[j]) for i in range(len(f)) for j in range(i,len(f))]

plt.hist(lst,2048)
try:
        plt.savefig("hist.png")
except IOERROR:
        print "Error, cannot save"
        plt.show()
        sys.exit()

mean = np.average(lst)
std = np.std(lst)

print mean, std*std
