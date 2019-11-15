# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:34:48 2019

@author: MummLab
"""

import cv2
import numpy as np
cap1 = cv2.VideoCapture(1)
#cap2 = cv2.VideoCapture(2) #you can check what integer code the next camera uses
#cap2 = cv2.VideoCapture(2) #you can check what integer code the next camera uses
#and so on for other cameras
#You could also make this more convenient and more readable by using an array of videocapture objects

while True:
    ret1,img1=cap1.read()
    cv2.imshow('video output1',img1)
    k=cv2.waitKey(10)& 0xff
    if k==27:
        break
cap1.release()
cap2.release()
#and so on for the other cameras
cv2.destroyAllWindows()