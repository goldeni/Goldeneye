#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np

print sys.stdin
r = 4

def compare(a,b):
        a = a[1:-2].split(',')
        b = b[1:-2].split(',')
        "duuuude..."
        return reduce(lambda x,y:x+y,[int(a[i])^int(b[i]) for i in xrange(len(a))])/float(len(a))

f = open('codes.txt','r')
bigList = []*756
for line in f:
        k = line.split("_")
        p = int(k[0])
        c = line.split("\t")
        a = c[1]
        bigList.append([p,a])

cP = [[]]
for i in range(len(bigList)):
        m = bigList[i]
        print m[0]
        n = m[0]
        print n,n-1,"\n"
        cP[n-1].append(m[1])
#print cP
lst = []
for x in range(756):
        f = cP[x]
        #print "working: ",x,len(f)
        #lst.append([compare(f[i],f[j]) for i in range(len(f)) for j in range(i,len(f))])

plt.hist(lst,2048)
try:
        plt.savefig("matching-hist.png")
except IOERROR:
        print "Error, cannot save"
        plt.show()
        sys.exit()

mean = np.average(lst)
std = np.std(lst)

print mean, std*std
