import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
import random

import cv2
import pylab

def affiche3D(img, espacement):
    fig = pylab.figure()
    ax = Axes3D(fig)
    plt.axis("equal")
    X = []
    Y = []
    Z = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if i%espacement==0 and j%espacement==0:
                if img[i][j]!=0:
                    X.append(i)
                    Y.append(j)
                    Z.append(-img[i][j])
    ax.scatter(X, Y, Z)
    plt.show()