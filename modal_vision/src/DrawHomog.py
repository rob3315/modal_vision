import numpy as np
import cv2
from matplotlib import pyplot as plt

class DrawHomog(object):
    
    def __init__(self, calcHomog):
        [hmin, hmax, wmin, wmax] = calcHomog.path.corners
        self.H = hmax-hmin
        self.W = wmax-wmin
        self.trans = -hmin, -wmin
        
        
    def drawFinal():
        im_finale = np.zeros((H,W), np.uint8)
    
        