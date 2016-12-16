'''
Created on 16 déc. 2016

@author: remi
'''
import numpy as np

class Path(object):
    '''
    classdocs
    '''


    def __init__(self, h,w):
        '''
        Constructor to do
        '''
        self.listHomography=[np.eye(3)]# homogrpahy of the nth image from the FIRST
        self.corners=[0,h-1,0,w-1] #hmin,hmax,wmin,wmax
        self.h,self.w=h,w
    
    def add_homography(self,homography):
        h,w=self.h,self.w
        homo=np.dot(self.listHomography[-1],homography) #composition of the nth homography
        self.listHomography.append(homo)
        new_corner=np.array(map(lambda c:np.dot(homo,c),[[0,0,1],[h-1,0,1],[h-1,w-1,1],[0,w-1,1]]))
        new_corner=map(lambda x : x/x[2],new_corner)
        hm=min(min(map(lambda x : x[0],new_corner)),self.corners[0])
        hM=max(max(map(lambda x : x[0],new_corner)),self.corners[1])
        wm=min(min(map(lambda x : x[1],new_corner)),self.corners[2])
        wM=max(max(map(lambda x : x[1],new_corner)),self.corners[3])
        self.corners=[hm,hM,wm,wM]
        return