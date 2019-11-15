#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 12:28:27 2018

@author: mcdevitt
"""

import cv2
import os

directory = 'C:/Users/MummLab/Kyle/simpleware/p_metal_crop/'
directory2 = 'C:/Users/MummLab/Kyle/simpleware/p_metal_crop_clahe/'
clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(6,6))
 
for file in os.listdir(directory):
    print(file)
    img = cv2.imread(directory + file, 0)
    img = cv2.bilateralFilter(img, 4, 9, 9)
    img = clahe.apply(img)
    imgformat = '.tiff'
    cv2.imwrite(directory2 + file[:file.find('.')] + '_clahe' + imgformat, img)