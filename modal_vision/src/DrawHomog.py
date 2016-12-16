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
        
        
    def drawFinal(self):
        im_finale = np.zeros((self.W,self.H), np.uint8)
        
        img1 = cv2.imread('1.jpg',0)
        img2 = cv2.imread('2.jpg',0)
        img3 = cv2.imread('3.jpg',0)
     
        img1distorted = cv2.warpPerspective(img1, np.dot(self.Mtrans, self.calcHomog.path.listHomography[1-1]), (self.W,self.H))
        img2distorted = cv2.warpPerspective(img2, np.dot(self.Mtrans, self.calcHomog.path.listHomography[2-1]), (self.W,self.H))
        img3distorted = cv2.warpPerspective(img3, np.dot(self.Mtrans, self.calcHomog.path.listHomography[3-1]), (self.W,self.H))
        
        im_finale = img1distorted/3+img2distorted/3+img3distorted/3
        
        cv2.imshow("Image", im_finale)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("the end")
        
        
        
    
        