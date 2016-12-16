import numpy as np
import cv2
from matplotlib import pyplot as plt

from Path import Path

class CalcHomog(object):
   


    def __init__(self, firstImage):
        
        #SIFT and KTREE
        self.sift =  cv2.xfeatures2d.SIFT_create()
        FLANN_INDEX_KDTREE = 0
        self.MIN_MATCH_COUNT = 10
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        #infos suppl.
        self.h,self.w=firstImage.shape()

        #contiendra le chemin
        self.path=Path(self.h, self.w)
        
        
        
    def addImage(self, lastImage, nextImage): #HOMOGRAPHIE A APPLIQUER SUR L'IMAGE NEXTIMAGE...
    
        #chercher les features, les trier, les matcher
        kp1, des1 = self.sift.detectAndCompute(lastImage,None)
        kp2, des2 = self.sift.detectAndCompute(nextImage,None)
        matches12 = self.flann.knnMatch(des2,des1,k=2)
        good12 = []
        for m,n in matches12:
            if m.distance < 0.7*n.distance:
                good12.append(m)
                
        #SI OK
        if len(good12)>self.MIN_MATCH_COUNT:
            src_pts12 = np.float32([ kp2[m.queryIdx].pt for m in good12 ]).reshape(-1,1,2)
            dst_pts12 = np.float32([ kp1[m.trainIdx].pt for m in good12 ]).reshape(-1,1,2)
            M12, mask12 = cv2.findHomography(src_pts12, dst_pts12, cv2.RANSAC,5.0)
            matchesMask12 = mask12.ravel().tolist()
            self.path.add_homography(M12)
        #SINON
            ######################################A FAIRE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        #la classe Path va s'updater
        
        return
    def get_path(self):
        return self.path
    