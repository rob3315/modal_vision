'''
Created on 2 dec. 2016

@author: remi
'''
import numpy as np
import cv2
import matplotlib.pyplot as plt

def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out

img1 = cv2.imread("/Users/remi/workspace/dataset_slam_vertical/image/0002872-000004781872.jpg",0)
img2 = cv2.imread("/Users/remi/workspace/dataset_slam_vertical/image/0002884-000004801858.jpg",0)    
h=img2.shape[1]
w=img2.shape[0]
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)      # queryImage
# Initiate SIFT detector
orb = cv2.ORB()
cv2.imshow("img1",img1)

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# Match descriptors.
matches = bf.match(des1,des2)
# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)
# Draw first 10 matches.
img3 = drawMatches(img1,kp1,img2,kp2,matches[:10])
src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches[:10] ]).reshape(-1,1,2)
dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches[:10] ]).reshape(-1,1,2)
#print("hi")
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
#img3=cv2.warpPerspective(img1, M,(img1.shape[1],img1.shape[0]))
print(M,mask)
cv2.imshow("img3",img3)
cv2.imshow("img2",img2)
superposition = np.zeros((w,h,3), np.uint8)
for i in range(w):
    for j in range(h):
        #print(img2[i][j])
        #print(img3[i][j])
        superposition[i][j]=[img2[i][j],0,img3[i][j]]
cv2.imshow("sup",superposition) 
cv2.imwrite("/Users/remi/Documents/2A/modal_rapport/imgmatch.png",img3)
#cv2.imwrite("/Users/remi/Documents/2A/modal_rapport/superposition.png",superposition)

cv2.waitKey(0)