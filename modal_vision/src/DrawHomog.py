import numpy as np
import cv2
from matplotlib import pyplot as plt

class DrawHomog(object):
    
    def __init__(self, calcHomog):
        [wmin, wmax,hmin, hmax] = calcHomog.path.corners
        print(wmin, wmax)
        self.H = hmax-hmin
        self.W = wmax-wmin
        self.trans = -hmin, -wmin
        self.calcHomog = calcHomog
        self.Mtrans = [[1,0,-wmin],[0,1,-hmin],[0,0,1]]
        
        
    def drawFinal(self,lst_img):
        im_finale = np.zeros((self.W,self.H), np.uint8)
        lst_img_distorted=map(lambda img :cv2.warpPerspective(img, np.dot(self.Mtrans, self.calcHomog.path.listHomography[1-1]), (self.W,self.H)))        
        def f(x,y):
            if x==0: return y
            else : return (x+y)/2
        for i in range(self.W):
            for j in range(self.H):
                im_finale[i][j]=reduce(f,lst_img_distorted)
        cv2.imshow("Image", im_finale)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("the end")
        
        
        
    
        