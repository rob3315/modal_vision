import numpy as np
import cv2
from matplotlib import pyplot as plt
from numpy import uint8
from timeit import itertools

class DrawHomog(object):
    
    def __init__(self, calcHomog):
        [wmin, wmax,hmin, hmax] = calcHomog.path.corners
        print(wmin, wmax)
        self.H = hmax-hmin
        self.W = wmax-wmin
        self.trans = -hmin, -wmin
        self.calcHomog = calcHomog
        self.Mtrans = [[1,0,-wmin],[0,1,-hmin],[0,0,1]]
        
        
    def drawFinal(self,list_img):
        im_finale_0 = np.zeros((self.H,self.W), np.uint8)
        im_finale_1 = np.zeros((self.H,self.W), np.uint8)
        im_finale_2 = np.zeros((self.H,self.W), np.uint8)
        im_calque = np.zeros((self.H,self.W), np.uint8)
        first_calque=np.ones((list_img[0].shape[:2]),np.uint8)
        lst_calques=[]
        list_img_distorted=[]
        n=len(list_img)
        for i in range(n):
            print(self.calcHomog.path.listHomography[i])
            lst_calques.append(cv2.warpPerspective(first_calque, np.dot(self.Mtrans, self.calcHomog.path.listHomography[i]), (self.W,self.H)))
            list_img_distorted.append(cv2.warpPerspective(list_img[i], np.dot(self.Mtrans, self.calcHomog.path.listHomography[i]), (self.W,self.H)))
        for i in range(len(list_img_distorted)):    
            im_calque+=lst_calques[i]
        for i in range(self.H):
            for j in range(self.W):
                im_calque[i][j]=max(1,im_calque[i][j])
        for i in range(len(list_img_distorted)): 
            im_finale_0 += (list_img_distorted[i][:,:,0]/im_calque)
            im_finale_1 += (list_img_distorted[i][:,:,1]/im_calque)
            im_finale_2 += (list_img_distorted[i][:,:,2]/im_calque)
        im_finale=np.zeros((self.H,self.W,3))
        im_finale[:,:,0]=im_finale_0/255.
        im_finale[:,:,1]=im_finale_1/255.
        im_finale[:,:,2]=im_finale_2/255.
        #print(im_finale)
        #im_calque=np.reshape(map(lambda t:max(1,t),np.fromiter(im_calque)),(self.H,self.W))
                
        plt.imsave("/Users/remi/Desktop/couleur.jpg",im_finale)
        cv2.imshow("Image", im_finale)
