'''
Created on 6 janv. 2017

@author: remi
'''
import numpy as np
from CalcHomog import CalcHomog
import cv2
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from plot3D import *
import math

class DrawDepth(object):
    '''
    classdocs
    '''


    def __init__(self,calcHomog):
        [wmin, wmax,hmin, hmax] = calcHomog.path.corners
        self.H = hmax-hmin
        self.W = wmax-wmin
        self.trans = -hmin, -wmin
        self.calcHomog = calcHomog
        self.Mtrans = [[1,0,-wmin],[0,1,-hmin],[0,0,1]]
    def get_similitude(self,homog):
        seuil=0.001
        homog=homog/homog[2][2]
        if homog[2][0]<seuil and homog[2][1]<seuil:
            s=homog[0][0]*homog[1][1]-homog[1][0]*homog[0][1]
            rotation=np.array([[homog[0][0]/s,homog[0][1]/s,0],[homog[1][0]/s,homog[1][1]/s,0],[0,0,1/s]])
            translation=np.array([[homog[2][0],homog[2][1],1-1/s]])
            #print(rotation, translation)
            return np.append(rotation,np.transpose(translation),axis=1)
        else : print " not close to a similitude"   
    def get_scale(self,h):
        return math.sqrt(1.*h[0][0]*h[1][1]-1.*h[1][0]*h[0][1])
    def cameraPoseFromHomography(self,H):
        print(H)
        U,s,Vt=np.linalg.svd(H)
        print(U,s,Vt)
        V=np.transpose(Vt)
        S=np.array([[1-s[1]**2,1-s[0]**2,0],[1,1,1],[1-s[2]**2,0,1-s[0]**2]])
        N=np.linalg.solve(S,np.array([0,1,0]))
        print(N)
        N=np.sqrt(N)
        stheta=(s[0]-s[2])*N[0]*N[2] % (2*np.pi)
        ctheta=(s[1]**2-s[0]*s[2])/((s[0]+s[2])*s[1])
        if stheta>0:
            theta=np.arccos(ctheta)
        else:
            theta=np.pi+np.arccos(ctheta)
        return

 
    def drawFinal(self,list_img):
        #self.cameraPoseFromHomography(self.calcHomog.path.listHomography[1])
        im_finale = np.zeros((self.H,self.W), np.uint16)
        im_calque = np.zeros((self.H,self.W), np.uint16)
        lst_calques=[]
        list_img_distorted=[]
        n=len(list_img)
        m=np.median(list_img[0])
        s=[1]
        for i in range(n):
            #print(self.calcHomog.path.listHomography[i])
            first_calque=np.ones((list_img[0].shape),np.uint16)
            first_calque=np.minimum(first_calque,list_img[i])
            s.append(1*self.get_scale(self.calcHomog.path.listHomography[i]))
            c=np.int(m*(1-s[i]))
            lst_calques.append(cv2.warpPerspective(first_calque, np.dot(self.Mtrans, self.calcHomog.path.listHomography[i]), (self.W,self.H)))
            #list_img_distorted.append(cv2.warpPerspective(list_img[i]-c*first_calque, np.dot(self.Mtrans, self.calcHomog.path.listHomography[i]), (self.W,self.H)))
            list_img_distorted.append(cv2.warpPerspective(list_img[i], np.dot(self.Mtrans, self.calcHomog.path.listHomography[i]), (self.W,self.H)))
            print(c)
        for i in range(len(list_img_distorted)):    
            im_calque+=lst_calques[i]
        for i in range(self.H):
            for j in range(self.W):
                im_calque[i][j]=max(1,im_calque[i][j])
        print(s)
        for i in range(len(list_img_distorted)): 
            #plt.imshow(list_img_distorted[i])
            #plt.show()
            
            im_finale += (list_img_distorted[i]/im_calque)
#         for i in range(len(im_finale)):
#             for j in range(len(im_finale[0])):
#                 if im_finale[i][j]>=1500 or im_finale[i][j]<=800:
#                     im_finale[i][j]=500
        #im_calque=np.reshape(map(lambda t:max(1,t),np.fromiter(im_calque)),(self.H,self.W))
        cv2.imwrite("/Users/remi/Desktop/profondeurmod.png",im_finale)
        #plt.imshow(np.array(im_finale))
        #plt.show()
        #print(np.median(im_finale))
        affiche3D(im_finale, 10)
        #cv2.imshow("Depth", im_finale)
