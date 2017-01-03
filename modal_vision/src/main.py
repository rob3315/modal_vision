import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

from CalcHomog import CalcHomog
from DrawHomog import DrawHomog

def main():
    
    with open(os.getcwd()+"/liste.txt") as f:
        list_f_img = f.readlines()
        list_f_img = [line.split(' ') for line in list_f_img]
    list_f_img = ["img/"+x[0][:-1] for x in list_f_img]
    print(list_f_img)
    list_img = [cv2.imread(x,0) for x in list_f_img]
    list_img=list_img[1:4]
    
    calcHomog = CalcHomog(list_img[0])
    
    
    
    for i in range(len(list_img)-1):
        calcHomog.addImage(list_img[i], list_img[i+1])
    drawHomog = DrawHomog(calcHomog)
    drawHomog.drawFinal(list_img)

main()