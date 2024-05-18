# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import skimage.filters as skFilters
import skimage.io as skio
from skimage import morphology
# from skimage import feature
from skimage.segmentation import clear_border
from skimage.transform import rotate
from skimage import measure
# from skimage.color import label2rgb, rgb2gray
import math

def getWindow(pImg, row, col, winShape):
    offsetShape = (winShape[0]//2, winShape[1]//2)
    window = pImg[row-offsetShape[0]:row+offsetShape[0]+1, col-offsetShape[1]:col+offsetShape[1]+1]
    return window

def getPaddedImage(img, fltShape):
    inShape = img.shape
    padShape = (fltShape[0]//2, fltShape[1]//2)
    
    padImg = np.zeros(shape = (inShape[0] + (2*padShape[0]), 
                               inShape[1] + (2*padShape[1])), dtype=np.uint8)
    
    padImg[padShape[0]:-padShape[0], padShape[1]:-padShape[1]] = img
    return padImg

def getThresholdedImage(image):
    r = skFilters.threshold_otsu(image)
    binary_image = 1*(image > r)
    return binary_image

def isHit(window, SE):
    row, col = window.shape
    for r in range(0, row):
        for c in range(0, col):
            if(window[r, c] == 1 and SE[r, c] == 1):
                return True
    return False

def isFit(window, SE):
    row, col = window.shape
    for r in range(0, row):
        for c in range(0, col):
            if(window[r, c] == 0 and SE[r, c] == 1):
                return False
    return True

def erode(image, structuring_element):
    paddedImage = getPaddedImage(image, structuring_element.shape )
    erodedImage = np.zeros(shape=image.shape, dtype = np.uint8)
    row, col = erodedImage.shape
    for r in range(0, row):
        for c in range(0, col):
            if(r > 0 and c > 0):
                window = getWindow(paddedImage, r, c, structuring_element.shape)
                if(isFit(window, structuring_element)):
                    erodedImage[r, c] = 1
                else:
                    erodedImage[r, c] = 0
    return erodedImage
                
                
def dilate(image, structuring_element):
    paddedImage = getPaddedImage(image, structuring_element.shape)
    dilatedImage = np.zeros(shape=image.shape, dtype = np.uint8)
    row, col = dilatedImage.shape
    for r in range(0, row):
        for c in range(0, col):
            if(r > 0 and c > 0):
                window = getWindow(paddedImage, r, c, structuring_element.shape)
                if(isHit(window, structuring_element)):
                    dilatedImage[r, c] = 1
                else:
                    dilatedImage[r, c] = 0
    return dilatedImage
            


def getOpenedImage(image, se):
    opened = dilate(erode(image,se),se)
    return opened

def getClosedImage(image, se):
    closed = erode(dilate(image,se),se)
    return closed



image = skio.imread("super tota.jpg", as_gray=True);
#  Structuring Element
se  = np.ones(shape=(5,5), dtype=np.uint8)

# Thresholded Image
thresholded = getThresholdedImage(image)
# removing objects that are touching the border
edge_touching_removed = clear_border(thresholded)
plt.imshow(thresholded, cmap='gray')
# opened = getOpenedImage(edge_touching_removed, se)
# plt.imshow(opened, cmap='gray')

# plt.title("Opened Image")
# closed = morphology.binary_closing(edge_touching_removed, se)
# plt.imshow(closed, cmap='gray')
# plt.title("Closed Image")


# Labeling regions
labeled_image = measure.label(edge_touching_removed, connectivity=image.ndim)
props = measure.regionprops_table(labeled_image, image,
                                  properties = ['label',
                                                'area',
                                                'bbox',
                                                'major_axis_length',
                                                'minor_axis_length',
                                                'orientation',
                                            
                                                ])
import pandas as pd
df = pd.DataFrame(props)
angles = df['orientation']
angles = list((angles))
size = df.shape[0]
angles_degree = np.array(angles)
for i in range(0,size):
      angles_degree[i] = math.degrees(angles_degree[i])
     
df['angle_degrees'] = angles_degree
objects = df[df['area'] > 1000].to_numpy()
label = 0
area = 1
bbox0 = 2
bbox1 = 3
bbox2 = 4
bbox3 = 5
orientation = 6
angleDegree = 7
maxArea = np.max(objects[:, area])
print(maxArea)

row,col = objects.shape
for r in range(0, row):
    checkArea = objects[r, area]
    if(checkArea < maxArea):
        b0 = int(objects[r, bbox0]) 
        b1 = int(objects[r, bbox1]) 
        b2 = int(objects[r, bbox2])
        b3 = int(objects[r, bbox3]) 
        angle = objects[r, angleDegree]
        cropped = edge_touching_removed[b0:b2, b1:b3]
        cropped = rotate(cropped, 360-angle)
        plt.figure(dpi=200)
        plt.imshow(cropped, cmap='gray')
        


import csv 
fields = ['label','area','bbox-0','bbox-1','bbox-2','bbox-3','orientation']
outfile = open('check.csv','w')
writer = csv.writer(outfile) 
writer.writerow(fields)
writer.writerows(objects)
outfile.close()

    
    


