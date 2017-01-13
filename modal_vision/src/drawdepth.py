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
    def cameraPoseFromHomography(self,H):
    
        pose = np.eye(3, 4)  # 3x4 matrix, the camera pose
        norm1 = np.linalg.norm(H[:, 0])  
        norm2 = np.linalg.norm(H[:, 1])  
        tnorm = (norm1 + norm2) / 2;  # Normalization value
    
        p1 = H[:, 0]  # Pointer to first column of H
        p2 = pose[:, 0]  # Pointer to first column of pose (empty)
        #cv2.normalize(p1, p2);  # Normalize the rotation, and copies the column to pose
    
        p1 = H[:1]  # Pointer to second column of H
        p2 = pose[:, 1]  # Pointer to second column of pose (empty)
    
        #cv2.normalize(p1, p2);  # Normalize the rotation and copies the column to pose
    
        p1 = pose[:, 0]
        p2 = pose[:, 1]
    
        p3 = np.cross(p1, p2)  # Computes the cross-product of p1 and p2
        c2 = pose[:, 2]  # Pointer to third column of pose
        p3.copyTo(c2)  # Third column is the crossproduct of columns one and two
    
        pose[:, 3] = H[:, 2] / tnorm;  # vector t [R|t] is the last column of pose
        
        return pose

 
    def drawFinal(self,list_img):
        im_finale = np.zeros((self.H,self.W), np.uint16)
        im_calque = np.zeros((self.H,self.W), np.uint16)
        lst_calques=[]
        list_img_distorted=[]
        n=len(list_img)
        for i in range(n):
            #print(self.calcHomog.path.listHomography[i])
            first_calque=np.ones((list_img[0].shape),np.uint16)
            first_calque=np.minimum(first_calque,list_img[i])
            lst_calques.append(cv2.warpPerspective(first_calque, np.dot(self.Mtrans, self.calcHomog.path.listHomography[i]), (self.W,self.H)))
            list_img_distorted.append(cv2.warpPerspective(list_img[i], np.dot(self.Mtrans, self.calcHomog.path.listHomography[i]), (self.W,self.H)))
        for i in range(len(list_img_distorted)):    
            im_calque+=lst_calques[i]
        for i in range(self.H):
            for j in range(self.W):
                im_calque[i][j]=max(1,im_calque[i][j])
        for i in range(len(list_img_distorted)): 
            #plt.imshow(list_img_distorted[i])
            #plt.show()
            im_finale += (list_img_distorted[i]/im_calque)
#         for i in range(len(im_finale)):
#             for j in range(len(im_finale[0])):
#                 if im_finale[i][j]>=1500 or im_finale[i][j]<=800:
#                     im_finale[i][j]=500
        #im_calque=np.reshape(map(lambda t:max(1,t),np.fromiter(im_calque)),(self.H,self.W))
        cv2.imwrite("/Users/remi/Desktop/profondeur.png",im_finale)
        plt.imshow(np.array(im_finale))
        plt.show()
        #cv2.imshow("Depth", im_finale)
