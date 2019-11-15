# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 15:36:04 2019

@author: MummLab
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

figure = plt.figure(constrained_layout=True, figsize=(6.5,10))
spec2 = gridspec.GridSpec(ncols=12, nrows=3, figure=figure)

gs0 = gridspec.GridSpec(ncols=4, nrows=3, figure=figure)

gs11 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[0])
gs12 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[1])
gs13 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[2])
gs14 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[3])
gs21 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[4])
gs22 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[5])
gs23 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[6])
gs24 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[7])
gs31 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[8])
gs32 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[9])
gs33 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[10])
gs34 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=1, subplot_spec=gs0[11])


ax211 = figure.add_subplot(gs11[0,0])
ax212 = figure.add_subplot(gs12[0,0])
ax213 = figure.add_subplot(gs13[0,0])
ax214 = figure.add_subplot(gs14[0,0])

ax221 = figure.add_subplot(gs21[0,0])
ax222 = figure.add_subplot(gs22[0,0])
ax223 = figure.add_subplot(gs23[0,0])
ax224 = figure.add_subplot(gs24[0,0])

ax231 = figure.add_subplot(gs31[0,0])
ax232 = figure.add_subplot(gs32[0,0])
ax233 = figure.add_subplot(gs33[0,0])
ax234 = figure.add_subplot(gs34[0,0])

ax311 = figure.add_subplot(gs11[0,1:3])
ax312 = figure.add_subplot(gs12[0,1:3])
ax313 = figure.add_subplot(gs13[0,1:3])
ax314 = figure.add_subplot(gs14[0,1:3])

ax321 = figure.add_subplot(gs21[0,1:3])
ax322 = figure.add_subplot(gs22[0,1:3])
ax323 = figure.add_subplot(gs23[0,1:3])
ax324 = figure.add_subplot(gs24[0,1:3])

ax331 = figure.add_subplot(gs31[0,1:3])
ax332 = figure.add_subplot(gs32[0,1:3])
ax333 = figure.add_subplot(gs33[0,1:3])
ax334 = figure.add_subplot(gs34[0,1:3])


axes1 = [ax211, ax212, ax213, ax214,
         ax221, ax222, ax223, ax224,
         ax231, ax232, ax233, ax234,
         ]

axes2 = [ax311, ax312, ax313, ax314,
         ax321, ax322, ax323, ax324,
         ax331, ax332, ax333, ax334,
         ]


figure.show()