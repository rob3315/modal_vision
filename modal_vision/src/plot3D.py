from matplotlib import pyplot
import pylab
from mpl_toolkits.mplot3d import Axes3D
import random

import cv2
import pylab

img = cv2.imread("depth_2.png", cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)



fig = pylab.figure()
ax = Axes3D(fig)

X = []
Y = []
Z = []


for i in range(360):
    for j in range(480):
        if img[i][j]!=0:
            X.append(i)
            Y.append(j)
            Z.append(img[i][j])
            
print(X,Y,Z)

ax.scatter(X, Y, Z)
pyplot.show()