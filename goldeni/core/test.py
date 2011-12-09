#!/usr/bin/python

import sys

f = open('codes.txt','r')
#f = [i for i in n]
g = open('irisCodes.csv','w')
for i in f:
        pS = i.split('_')
        p = pS[0]

        iS = i.split('\t')
        iC = iS[1]

        iC = iC[1:-2].split(',')
        iC = [int(j) for j in iC]
        iCS = ''.join([str(i) for i in iC])
        print len(iCS)
        g.write(str(int(p)) + ',' + iCS + '\n')

g.close()
f.close()
