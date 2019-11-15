#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:30:58 2018
@author: mcdevitt
"""
import numpy as np
from zipfile import ZipFile
from matplotlib.font_manager import FontProperties
import matplotlib
import os

tmpdir = 'C:/tmp/gasevo/'
if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)

o2_e = 0.401 - 0.235   # formal potential of O2 evolution (with ref correction)
h2_e = -0.829 - 0.235  # formal potential of H2 evolution (with ref correction)

font = FontProperties()
font.set_name('Sans-Serif')
matplotlib.rcParams['font.sans-serif'] = "Arial"

alpha = 0.4

colors1 = {
           '1':'#FFD200',
           '5':'#0063A4',
           '10':'#FF0000',
           '25':'#00CD00',
           '50':'#FF8E00',
           '100':'#6E00AB',
           '250':'#B1F200'
           }
colors2 = {
           '1':'#FFEC93',
           '5':'#1392E5',
           '10':'#FF0606',
           '25':'#06F006',
           '50':'#FF9106',
           '100':'#9B12E7',
           '250':'#BAFB06'
           }
colors3 = {
           '1':'#C8A500',
           '5':'#003B61',
           '10':'#980000',
           '25':'#007900',
           '50':'#985500',
           '100':'#410065',
           '250':'#698F00'
           }

gstatcolors = {
               '10':'#0063A4',
               '20':'#FF0000',
               '30':'#00CD00',
               }

gstatcolors2 = {'10':['#73a9cd', '#5c9bc5', '#458dbc', '#2e7fb4', '#1771ac', '#0063a4', '#005a96',
                      '#005287', '#004978', '#004069', '#00365a', '#002d4b', '#00243c', '#001b2d'],
                '20':['#ff7373', '#ff5c5c', '#ff4545', '#ff2e2e', '#ff1717', '#ff0000', '#e80000',
                      '#d10000', '#ba0000', '#a30000', '#8c0000', '#740000', '#5d0000', '#460000'],
                '30':['#73e373', '#5cdf5c', '#45da45', '#2ed62e', '#17d117', '#00cd00', '#00bb00',
                      '#00a800', '#009600', '#008300', '#007000', '#005e00', '#004b00', '#003800']}

def importdata(file_path):
    runs = {}
    out = {}
    with ZipFile(file_path, 'r') as zip:
        indices = [s for s in zip.namelist() if ".mpro" in s]
        for i in indices:
            run = i[:5]
            globals()[run] = {}
            steplist = []
            with zip.open(i) as experiments:
    #            print(experiments)
    #            open(experiments)
                buffer = []
                keepCurrentSet = True
                for line in experiments:
                    buffer.append(line)
                    if line.startswith(b"  Begin Experiment:           "):
                        steplist.append(line[30:])
            runs[str(i)[:5]] = steplist
        steplist = [s for s in zip.namelist() if ".cor" in s]
        for i in steplist:
            with zip.open(i) as step:
                run = i[:5]
                buffer = []
                keepCurrentSet = True
                n = 0
                for line in step:
                    if n == 1:
                        buffer.append(line)
                    if line.startswith(b"End Header:"):
                        n = 1
                out[str(i)[str(i).find("Step"):-4]] = np.genfromtxt(buffer)
        
    return out, runs[i[:5]]

def half_sample_mode(x, already_sorted=False):
    x = x[~np.isnan(x)]
    if len(x) < 3:
        return np.mean(x)
    if already_sorted:
        sorted_x = x # No need to sort
    else:
        sorted_x = np.sort(x)
    half_idx = int((len(x) + 1) / 2) # Round up to include the middle value,
                                     # in the case of an odd-length array

    # Calculate all interesting ranges that span half of all data points
    ranges = sorted_x[-half_idx:] - sorted_x[:half_idx]
    smallest_range_idx = np.argmin(ranges)

    # Now repeat the procedure on the half that spans the smallest range
    x_subset = sorted_x[smallest_range_idx : (smallest_range_idx+half_idx)]
    return half_sample_mode(x_subset, already_sorted=True)