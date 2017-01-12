'''
Created on 6 janv. 2017

@author: remi
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
img=cv2.imread("/Users/remi/workspace/dataset_slam_vertical/modalSLAM/seq2/depth/0000034-000000054999.png",cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

print(len(np.ndarray.flatten(img)))
lst=np.ndarray.flatten(img)
new_lst=[]
#for i in range(len(lst)):
#    if True:#lst[i]>1000:
#        new_lst.append(min(max((lst[i]-1000),0)/4,255))
print(img.shape)
#img2=np.reshape(new_lst, img.shape)
print(np.array(img))
plt.imshow(np.array(img))
#plt.hist(new_lst)
plt.show()
#plt.hist(x, bins, range, normed, weights, cumulative, bottom, histtype, align, orientation, rwidth, log, color, label, stacked, hold, data)
#plt.show()