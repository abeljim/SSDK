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

tmpdir = '/tmp/gasevo/'
if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)

o2_e = 0.401 - 0.235   # formal potential of O2 evolution (with ref correction)
h2_e = -0.829 - 0.235  # formal potential of H2 evolution (with ref correction)
h2_e_acid = 0 - 0.235  # acid potential of H2 evolution (with ref correction)

font = FontProperties(size=8)
font.set_name('Sans-Serif')
matplotlib.rcParams['font.sans-serif'] = "Arial"

alpha = 0.4
textposx, textposy = 0.075, 0.9
figsizex, figsizey = 3.25, 2.5
dblfigsizex, figsizey = 6.5, 2.5

left=0.1
bottom=0.25
wspace=0.1

dblleft=0.1
dblbottom=0.15
wspace=0.1

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
colors4 = ['#FFF0F0',
           '#FFE0E0',
           '#FFD1D1',
           '#FFC2C2',
           '#FFB3B3',
           '#FFA3A3',
           '#FF9494',
           '#FF8585',
           '#FF7575',
           '#FF6666',
           '#E65C5C',
           '#CC5252',
           '#B34747',
           '#993D3D',
           '#803333',
           '#662929',
           '#4C1F1F',
           '#331414',
           '#190A0A',
           '#000000']

colors5 = ['#53dd6c',
           '#63a088',
           '#56638a',
           '#483a58',
           '#56203d',
           ]
           
gstatcolors = {
               '10':'#0063A4',
               '20':'#FF0000',
               '30':'#00CD00',
               }
typecolors = {
              'bijel':['#73a9cd', '#5c9bc5', '#458dbc', '#2e7fb4', '#1771ac', '#0063a4', '#005a96',
                       '#005287', '#004978', '#004069', '#00365a', '#002d4b', '#00243c', '#001b2d'],
              'planar':['#ff7373', '#ff5c5c', '#ff4545', '#ff2e2e', '#ff1717', '#ff0000', '#e80000',
                       '#d10000', '#ba0000', '#a30000', '#8c0000', '#740000', '#5d0000', '#460000'],
              'powder':['#73e373', '#5cdf5c', '#45da45', '#2ed62e', '#17d117', '#00cd00', '#00bb00',
                       '#00a800', '#009600', '#008300', '#007000', '#005e00', '#004b00', '#003800'],
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

def importdata2(file_path):
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
                out[str(i)[str(i).find("scratches"):-4]] = np.genfromtxt(buffer)
        
    return out, runs[i[:5]]

