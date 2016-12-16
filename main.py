import numpy as np
import cv2
from matplotlib import pyplot as plt

from CalcHomog import CalcHomog


def main():
    
    img1 = cv2.imread('1.jpg',0)
    calcHomog = CalcHomog(img1)
    
    img2 = cv2.imread('2.jpg',0)
    calcHomog.addImage(img1,img2)