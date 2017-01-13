import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

from CalcHomog import CalcHomog
from DrawHomog import DrawHomog
from drawdepth import DrawDepth
import sys, glob, copy

def main():
    
    #with open(os.getcwd()+"/liste.txt") as f:
    path = "/Users/remi/workspace/dataset_slam_vertical/modalSLAM/seq2/"
    with open(path+"liste.txt") as f:
        list_f_img = f.readlines()
        list_f_img = [line.split(' ') for line in list_f_img]
    #list_f_img = ["img/"+x[0][:-1] for x in list_f_img]
    list_f_img=list_f_img[1:]
    list_f_depth = []
    list_f_img = [path+"image/"+x[0][:-1] for x in list_f_img]
    for a in list_f_img:
        list_f_depth.append(find_depth(path+"depth/", a))
    print(list_f_depth)
    print(list_f_img)
    list_img_brut = [cv2.imread(x,0) for x in list_f_img]
    list_img=[]
    print('a',len(list_img_brut))
    for a in list_img_brut:
        list_img.append(cv2.resize(a,(480,360)))
        print('a',len(list_img))
    list_depth=[cv2.imread(x,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH) for x in list_f_depth]
#     for i in range(len(list_img)):
#         print(i)
#         plt.figure(1)
#         plt.imshow(list_img[i])
#         plt.figure(2)
#         plt.imshow(list_depth[i])
#         plt.show()
    
    calcHomog = CalcHomog(list_img[0])
    
    
    
    
    for i in range(len(list_img)-1):
        calcHomog.addImage(list_img[i], list_img[i+1])
    drawHomog = DrawHomog(calcHomog)
    drawHomog.drawFinal(list_img)
    drawDepth = DrawDepth(calcHomog)
    #for h in calcHomog.path.listHomography:
        #print(drawDepth.cameraPoseFromHomography(h))
    drawDepth.drawFinal(list_depth)
    #cv2.waitKey(0)

def find_depth(path,colorfile):
    """file : name of the image.jpg, path : repository of the depth image"""
    filenames_depth=glob.glob(path+"*")
    ts_rgb = int(colorfile.split("-")[-1].split(".")[0])/2
    result=""
    ts_depth_closest = 0
    for id_img_depth,filename_depth in enumerate(filenames_depth):
        ts_depth = int(filename_depth.split("-")[-1].split(".")[0])
        if abs(ts_rgb-ts_depth)<=abs(ts_rgb-ts_depth_closest):
            ts_depth_closest = ts_depth
            result = filename_depth
    return result

main()