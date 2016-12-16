import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

#imagesdebasetest
img1 = cv2.imread('1.jpg',0)
img2 = cv2.imread('2.jpg',0)
img3 = cv2.imread('3.jpg',0)

# Initiate SIFT detector
sift =  cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
kp3, des3 = sift.detectAndCompute(img3,None)
    


#INITFLANN
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)



#1->2
matches12 = flann.knnMatch(des2,des1,k=2) # ATTENTION INVERSE TUTORIAL 2 -> 1
good12 = []
for m,n in matches12:
    if m.distance < 0.7*n.distance:
        good12.append(m)
if len(good12)>MIN_MATCH_COUNT:
    src_pts12 = np.float32([ kp2[m.queryIdx].pt for m in good12 ]).reshape(-1,1,2)
    dst_pts12 = np.float32([ kp1[m.trainIdx].pt for m in good12 ]).reshape(-1,1,2)
    M12, mask12 = cv2.findHomography(src_pts12, dst_pts12, cv2.RANSAC,5.0)
    matchesMask12 = mask12.ravel().tolist()


#2->3
matches23 = flann.knnMatch(des3,des2,k=2)
good23 = []
for m,n in matches23:
    if m.distance < 0.7*n.distance:
        good23.append(m)        
if len(good23)>MIN_MATCH_COUNT:
    src_pts23 = np.float32([ kp3[m.queryIdx].pt for m in good23 ]).reshape(-1,1,2)
    dst_pts23 = np.float32([ kp2[m.trainIdx].pt for m in good23 ]).reshape(-1,1,2)
    M23, mask23 = cv2.findHomography(src_pts23, dst_pts23, cv2.RANSAC,5.0)
    matchesMask23 = mask23.ravel().tolist()
    
    
#ASSEMBLAGE
    im_dst = np.zeros((900,900), np.uint8)    
    
    h,w=img1.shape #toutes meme taille ?
    coinHautDroit = (w,0,1)
    coinBasDroit = (w,h,1)
    finalCoinHautDroit = np.dot(M12, coinHautDroit)
    finalCoinBasDroit = np.dot(M12, coinBasDroit)
    
    #im_dst[0:h, 0:w]=img1/2
    
    cv2.warpPerspective(img2, M12, (900,900), im_dst)
    
    x,y,z=finalCoinHautDroit
    print(finalCoinHautDroit)
    x,y=x/z,y/z
    #print(im_dst)
    
    im_dst[y:y+3,x:x+3]=255
    
    
    
    cv2.imshow('Image', im_dst)

#    h,w = img1.shape
#    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#    dst = cv2.perspectiveTransform(pts,M12)
#
#    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print "Not enough matches are found - %d/%d" % (len(good12),MIN_MATCH_COUNT)
    matchesMask = None
draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask12, # draw only inliers
                   flags = 2)
                  

cv2.waitKey(5000)
cv2.destroyAllWindows()
print("the end")