#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Jun  3 12:34:33 2019
@author: mcdevitt
"""

import numpy as np
import os
import subprocess
import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
import matplotlib.ticker as mticker

def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    return a, b

tmpdir = '/tmp/frames/'
rootdir = '/Users/MummLab/Pictures/Calibration Curve/'
if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)
    
if not os.path.exists(rootdir):
    os.makedirs(rootdir)


##############################################################################
##############################################################################
#                   Variables section
##############################################################################
##############################################################################


#            [dimensions], threshold, name
#           dimensions are measured from the top left
#            xmin, xmax, ymin, ymax
standard = {#'ME':([1850, 3400, 900, 1900], 185, 'Microelectrode'),
            #'CC.F1':([1400,3400,670,2495], 185, 'Straight bar, Forward Sweep'),
            #'CC.R1':([1400,3400,670,2495], 170, 'Straight bar, Reverse Sweep'),
            'CC.F2':([1500,3500,575,2500], 185, 'Straight bar, Forward Sweep'),
            #'CC.F3':([1400,3600,470,2295], 172, 'Scratched bar, Forward Sweep')
           }

samples = {
           }

##############################################################################
##############################################################################
#                   Standard Calibration Section
##############################################################################
##############################################################################


for sample in standard.keys():
    runlist = [0, 25, 50, 100, 150, 200, 250, 300]
    ME_fig, ax = plt.subplots(figsize=(3.307, 2.48))
    sampledir = rootdir + sample + '/'
    dim = standard[sample][0]
    threshold = standard[sample][1]
    area = ((dim[1]-dim[0])*(dim[3]-dim[2]))
    results = []
    boxes = []
    banner = np.array(np.zeros(3456), ndmin=2).T
    banner2 = np.array(np.zeros(dim[3]-dim[2]), ndmin=2).T
    for run in runlist:
        fig, ax2 = plt.subplots()
        wdir = sampledir + str(run) + '/'
        results1 = []
        filelist = [f for f in os.listdir(wdir)
                    if os.path.isfile(os.path.join(wdir, f))]
        filelist.sort()
        filelist = [f for f in filelist if f != 'Thumbs.db']
        filelist = [f for f in filelist if f != 'latency.svg']
        filelist = [f for f in filelist if f != str(run) + '_' + 'overtime.svg']
        
        print('I found ' +
              str(len(filelist)) +
              ' frames in your ' + sample + ' ' + str(run) + 'μA directory!')
        print('Let\'s analyze them...')
        try:
            img = cv2.imread(wdir + filelist[len(filelist)//2], 0)[:, dim[0]:dim[1]]
        except:
            print("looks like you need to do " + sample + ' ' + str(run))
            img = np.ones((dim[3]-dim[2]), (dim[1]-dim[0]))
        banner = np.concatenate((banner, img), axis=1)
        banner2 = np.concatenate((banner2,cv2.threshold(img[dim[2]:dim[3],:],
                                                        threshold,
                                                        255,
                                                        cv2.THRESH_BINARY)[1]),
                                 axis=1)
        banner = np.concatenate((banner,
                                 np.array(np.zeros(banner.shape[0]),
                                          ndmin=2).T),
                                axis=1)
        banner2 = np.concatenate((banner2,
                                  np.array(np.zeros(banner2.shape[0]),
                                           ndmin=2).T),
                                 axis=1)
        print(filelist)
        for file in filelist:
            filename = wdir +file
            img = cv2.imread(filename, 0)[dim[2]:dim[3], 
                                          dim[0]:dim[1]]
            ret, thresh1 = cv2.threshold(img,
                                         threshold,
                                         255,
                                         cv2.THRESH_BINARY)
            results1.append(np.sum(len(np.where(thresh1 == 0)[0]))/area)
            ax.scatter(run, np.sum(len(np.where(thresh1 == 0)[0]))/area,
                            color='green',
                            alpha=0.05)
        #plt.imsave('/tmp/threshold.png', thresh1, cmap='gray')
        boxes.append(list(results1))
        ax2.scatter(np.arange(0, 500, 5), results1)
        ax2.set_ylim(0,0.04)
        ax2.set_title(standard[sample][2] + ', ' + str(run) + '$\mu$A')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Black level in frame')
        fig.savefig(sampledir + str(run) + '_' + 'overtime.svg')
    
    plt.imsave(sampledir + 'examples.png', banner, format='png', cmap='gray')
    plt.imsave(sampledir + 'examples.png', banner, format='png', cmap='gray')
    plt.imsave(sampledir + 'threshold.png', banner2, format='png', cmap='gray')
    results1 = np.asarray(results1)
    results.append([run,np.mean(results1),np.std(results1)])
    np.savetxt(sampledir + str(run) + '_results.csv',
               results1,
               delimiter=',')
    results = np.asarray(results)
    
    #a, b = best_fit(results[:,0], results[:,1])
    #yfit = [a + b * xi for xi in results[:,0]]
    #ax1.errorbar(results[:,0], results[:,1],
    #             yerr=results[:,2], fmt='ro', color='red')
    
    #ax1.plot(results[:,0], yfit, color='black', linestyle=':', alpha=0.5)
    
    ax.boxplot(boxes,
               positions=runlist,
               widths = 10,
               showfliers = False,
               whis=[10,90])
    ax.set_title(standard[sample][2] + ' (Standard)')
    ax.set_xlabel('Current ($\mu$A)')
    ax.set_ylabel('Black level in frame')
    ax.set_ylim([-0.0001, 0.025])
    ax.set_xlim([0, 350])
    ME_fig.savefig(sampledir + 'calibration_short.svg')











##############################################################################
##############################################################################
#               Standard Calibration Section (gray level)
##############################################################################
##############################################################################


for sample in standard.keys():
    runlist = [0, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    ME_fig, ax = plt.subplots()
    sampledir = rootdir + sample + '/'
    dim = standard[sample][0]
    #threshold = standard[sample][1]
    #area = ((dim[1]-dim[0])*(dim[3]-dim[2]))
    boxes = []
    #banner = np.array(np.zeros(3456), ndmin=2).T
    #banner2 = np.array(np.zeros(dim[3]-dim[2]), ndmin=2).T
    for run in runlist:
        data = []
        wdir = sampledir + str(run) + '/'
        results1 = []
        filelist = [f for f in os.listdir(wdir)
                    if os.path.isfile(os.path.join(wdir, f))]
        filelist.sort()
        print('I found ' +
              str(len(filelist)) +
              ' frames in your ' + sample + ' ' + str(run) + 'μA directory!')
        print('Let\'s analyze them...')
        try:
            img = cv2.imread(wdir + filelist[50], 0)[:, dim[0]:dim[1]]
        except:
            print("looks like you need to do " + sample + ' ' + str(run))
            img = np.ones((dim[3]-dim[2], (dim[1]-dim[0])))
        for file in filelist:
            filename = wdir + file
            data.append(cv2.imread(filename, 0)[dim[2]:dim[3],
                                                dim[0]:dim[1]])

        if run == 0:
            baseline = (np.mean(np.asarray(data), axis=0))
        else:
            for item in data:
                level = np.mean(baseline-item)
                ax.scatter(run, level,
                           color='green',
                           alpha=0.05)
                boxes[-1].append(np.mean(level))
        boxes.append(list())

    #a, b = best_fit(results[:,0], results[:,1])
    #yfit = [a + b * xi for xi in results[:,0]]
    #ax1.errorbar(results[:,0], results[:,1],
    #             yerr=results[:,2], fmt='ro', color='red')
    
    #ax1.plot(results[:,0], yfit, color='black', linestyle=':', alpha=0.5)
    """
    ax.boxplot(boxes[:-1],
               positions=runlist[1:],
               widths = 10,
               showfliers = False,
               whis=[10,90])
    """
    ax.set_title(standard[sample][2] + ' (Standard)')
    ax.set_xlabel('Current ($\mu$A)')
    ax.set_ylabel('Difference from Baseline')
    #ax.set_ylim([-0.0001, 0.05])
    ax.set_xlim([0, 600])
    ME_fig.savefig(sampledir + 'calibration_2.svg')
    ME_fig.savefig('/home/mcdevitt/Dropbox/UCI/Research/McDevitt Bijel Electrodes/Data/Gas evolution/image analysis/calibrationbar2.svg')


##############################################################################
##############################################################################
#                   Porous electrode calibration section
##############################################################################
##############################################################################

runlist = [0,
           25,
           50,
           100,
           250,
           500,
           ]
# dim = [xmin, xmax, ymin, ymax]  # y is indexed from the top!


figure = plt.figure(constrained_layout=True, figsize=(6.5,5))
gs0 = gridspec.GridSpec(ncols=3, nrows=2, figure=figure)

ax11 = figure.add_subplot(gs0[0,0])
ax12 = figure.add_subplot(gs0[0,1])
ax13 = figure.add_subplot(gs0[0,2])
ax21 = figure.add_subplot(gs0[1,0])
ax22 = figure.add_subplot(gs0[1,1])
ax23 = figure.add_subplot(gs0[1,2])

## Calibration plot section
axes = figure.axes
n = 0
for sample in samples.keys():
    sampledir = rootdir + sample + '/'
    dim = samples[sample][0]
    threshold = samples[sample][1]
    area = ((dim[1]-dim[0])*(dim[3]-dim[2]))
    results = []
    boxes = []
    banner = np.array(np.zeros(3456), ndmin=2).T
    banner2 = np.array(np.zeros(dim[3]-dim[2]), ndmin=2).T
    for run in runlist:
        wdir = sampledir + str(run) + '/'
        results1 = []
        filelist = [f for f in os.listdir(wdir)
                    if os.path.isfile(os.path.join(wdir, f))]
        filelist.sort()
        print('I found ' +
              str(len(filelist)) +
              ' frames in your ' +
              sample + ' ' + str(run) + 'μA'
              ' directory!')
        print('Let\'s analyze them...')
        try:
            img = cv2.imread(wdir + filelist[50], 0)[:, dim[0]:dim[1]]
        except:
            print("looks like you need to do " + sample + " " + str(run))
            img = np.ones((3456, (dim[1]-dim[0])))
        banner = np.concatenate((banner, img), axis=1)
        banner2 = np.concatenate((banner2,cv2.threshold(img[dim[2]:dim[3],:],
                                                        threshold,
                                                        255,
                                                        cv2.THRESH_BINARY)[1]),
                                 axis=1)
        banner = np.concatenate((banner,
                                 np.array(np.zeros(banner.shape[0]),
                                          ndmin=2).T),
                                axis=1)
        banner2 = np.concatenate((banner2,
                                  np.array(np.zeros(banner2.shape[0]),
                                           ndmin=2).T),
                                 axis=1)
        for file in filelist:
            filename = wdir + file
            img = cv2.imread(filename, 0)[dim[2]:dim[3],
                                          dim[0]:dim[1]]
            ret, thresh1 = cv2.threshold(img,
                                         threshold,
                                         255,
                                         cv2.THRESH_BINARY)
            results1.append(np.sum(len(np.where(thresh1 == 0)[0]))/area)
            axes[n].scatter(run, np.sum(len(np.where(thresh1 == 0)[0]))/area,
                            color='green',
                            alpha=0.05)
        #plt.imsave('/tmp/threshold.png', thresh1, cmap='gray')
        boxes.append(list(results1))
    plt.imsave(sampledir + 'examples.png', banner, format='png', cmap='gray')
    plt.imsave(sampledir + 'threshold.png', banner2, format='png', cmap='gray')
    results1 = np.asarray(results1)
    results.append([run,np.mean(results1),np.std(results1)])
    np.savetxt(sampledir + str(run) + '_results.csv',
               results1,
               delimiter=',')
    results = np.asarray(results)
    
    #a, b = best_fit(results[:,0], results[:,1])
    #yfit = [a + b * xi for xi in results[:,0]]
    #ax1.errorbar(results[:,0], results[:,1],
    #             yerr=results[:,2], fmt='ro', color='red')
    
    #ax1.plot(results[:,0], yfit, color='black', linestyle=':', alpha=0.5)
    
    axes[n].boxplot(boxes,
                    positions=runlist,
                    widths = 10,
                    showfliers = False,
                    whis=[10,90])
    axes[n].set_title(samples[sample][2])
    n = n + 1

for ax in [ax11, ax12, ax13]:
    ax.xaxis.set_major_formatter(mticker.NullFormatter())

for ax in [ax12, ax13, ax22, ax23]:
    ax.yaxis.set_major_formatter(mticker.NullFormatter())

for ax in figure.axes:
    ax.set_ylim([-0.0001, 0.05])
    ax.set_xlim([0, 600])

ax22.set_xlabel('Current ($\mu$A)')

figure.savefig(rootdir + 'calibration.svg', transparent=True)
"""
figure.text(0.03, 0.5,
            'Overpotential, $\eta$ ($mV$)',
            fontproperties=mdat.font,
            ha='center',
            va='center',
            rotation='vertical')
"""

##############################################################################
##############################################################################
#                               Decay Plots
##############################################################################
##############################################################################
"""
runlist = [
           'decay250',
           'decay100',
           'decay50'
           ]

for sample in samples.keys():
    sampledir = rootdir + sample + '/'
    dim = samples[sample][0]
    threshold = samples[sample][1]
    area = ((dim[1]-dim[0])*(dim[3]-dim[2]))

    fig2 = plt.figure(constrained_layout=True, figsize=(4, 9))
    spec2 = gridspec.GridSpec(ncols=1, nrows=3, figure=fig2)
    ax21 = fig2.add_subplot(spec2[0, 0])
    ax22 = fig2.add_subplot(spec2[1, 0])
    ax23 = fig2.add_subplot(spec2[2, 0])

    n=0
    
    for run in runlist:
        wdir = sampledir + run + '/'
        results = []
        filelist = [f for f in os.listdir(wdir) if os.path.isfile(os.path.join(wdir, f))]
        filelist.sort()
        print('I found '
              + str(len(filelist))
              + ' frames in your '
              + str(sample)
              + ' '
              + str(run)
              + ' directory!')
        print('Let\'s analyze them...')
        for file in filelist:
            filename = wdir + file
            stamp = os.path.getmtime(filename)
            img = cv2.imread(filename, 0)[dim[2]:dim[3],
                                          dim[0]:dim[1]]
            ret, thresh1 = cv2.threshold(img,
                                         threshold,
                                         255,
                                         cv2.THRESH_BINARY)
            time = int(file[6:-4])/1000
            results.append([time,
                            np.sum(len(np.where(thresh1 == 0)[0]))/area,
                            stamp])
        fig2.axes[n].scatter(np.asarray(results)[:,0],
                             np.asarray(results)[:,1],
                             alpha=0.1,
                             color='blue')
        np.savetxt(sampledir + '/' + run + '.txt', np.asarray(results))
        n=n+1
    ax22.set_ylabel('Bubble fraction in frame')
    ax23.set_xlabel('Time (s)')
    #plt.xscale('log')
    ax21.set_ylim([0.000, 0.008])
    ax22.set_ylim([0.000, 0.004])
    ax23.set_ylim([0.000, 0.002])
    for ax in fig2.axes:
        ax.set_xlim=(0.001,1300)
    fig2.savefig(sampledir + 'decayimg.svg', transparent=True)


##############################################################################
##############################################################################
#                               Startup Plots
##############################################################################
##############################################################################

runlist = [
           'start250',
           'start100',
           'start50'
           ]
n=0

for sample in samples.keys():
    sampledir = rootdir + sample + '/'
    dim = samples[sample][0]
    threshold = samples[sample][1]
    area = ((dim[1]-dim[0])*(dim[3]-dim[2]))

    fig3 = plt.figure(constrained_layout=True, figsize=(4, 9))
    spec3 = gridspec.GridSpec(ncols=1, nrows=3, figure=fig3)
    ax31 = fig3.add_subplot(spec3[0, 0])
    ax32 = fig3.add_subplot(spec3[1, 0])
    ax33 = fig3.add_subplot(spec3[2, 0])

    n=0
    
    for run in runlist:
        wdir = sampledir + run + '/'
        results = []
        filelist = [f for f in os.listdir(wdir) if os.path.isfile(os.path.join(wdir, f))]
        filelist.sort()
        print('I found '
              + str(len(filelist))
              + ' frames in your '
              + str(sample)
              + ' '
              + str(run)
              + ' directory!')
        print('Let\'s analyze them...')
        for file in filelist:
            filename = wdir + file
            img = cv2.imread(filename, 0)[dim[2]:dim[3],
                                          dim[0]:dim[1]]
            ret, thresh1 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            time = int(file[6:-4])/1000
            stamp = os.path.getmtime(filename)
            results.append([time,
                            np.sum(len(np.where(thresh1 == 0)[0]))/area,
                            stamp])
        fig3.axes[n].scatter(np.asarray(results)[:,0],
                             np.asarray(results)[:,1],
                             alpha=0.1,
                             color='red')
        np.savetxt(sampledir + '/' + run + '.txt', np.asarray(results))
        n=n+1
    ax32.set_ylabel('Bubble fraction in frame')
    ax33.set_xlabel('Time (s)')
    #plt.xscale('log')
    ax31.set_ylim([0.000, 0.008])
    ax32.set_ylim([0.000, 0.004])
    ax33.set_ylim([0.000, 0.002])
    for ax in fig3.axes:
        ax.set_xlim=(0.001,1300)
    fig3.savefig(sampledir + 'startimg.svg', transparent=True)

"""
##############################################################################
##############################################################################
#                               Combined
##############################################################################
##############################################################################

runlist = [
           'start250', 'decay250',
           'start100', 'decay100',
           'start50', 'decay50',
           ]

ymax = {'start250':0.04,
        'decay250':0.04,
        'start100':0.02,
        'decay100':0.02,
        'start50':0.01,
        'decay50':0.01}

n=0

for sample in samples.keys():
    sampledir = rootdir + sample + '/'
    dim = samples[sample][0]
    threshold = samples[sample][1]
    area = ((dim[1]-dim[0])*(dim[3]-dim[2]))

    fig4 = plt.figure(constrained_layout=True, figsize=(7, 9))
    spec4 = gridspec.GridSpec(ncols=2, nrows=3, figure=fig4)
    ax41 = fig4.add_subplot(spec4[0, 0])
    ax42 = fig4.add_subplot(spec4[0, 1])
    ax43 = fig4.add_subplot(spec4[1, 0])
    ax44 = fig4.add_subplot(spec4[1, 1])
    ax45 = fig4.add_subplot(spec4[2, 0])
    ax46 = fig4.add_subplot(spec4[2, 1])

    n=0
    
    for run in runlist:
        wdir = sampledir + run + '/'
        results = []
        filelist = [f for f in os.listdir(wdir) if os.path.isfile(os.path.join(wdir, f))]
        filelist.sort()
        print('I found '
              + str(len(filelist))
              + ' frames in your '
              + str(sample)
              + ' '
              + str(run)
              + ' directory!')
        print('Let\'s analyze them...')

        if 'start' in run:
            color = ['#ff7373','#ff1717', '#ba0000', '#5d0000']
        else:
            color = ['#73a9cd', '#1771ac', '#004978', '#004069']
        for file in filelist:
            filename = wdir + file
            img = cv2.imread(filename, 0)[dim[2]:dim[3],
                                          dim[0]:dim[1]]
            ret, thresh1 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            time = int(file[6:-4])/1000
            stamp = os.path.getmtime(filename)
            results.append([time,
                            np.sum(len(np.where(thresh1 == 0)[0]))/area,
                            stamp])
        fig4.axes[n].scatter(np.asarray(results)[:,0],
                             np.asarray(results)[:,1],
                             alpha=0.1,
                             color=color[0])
        fig4.axes[n].set_xlim((0,1300))
        fig4.axes[n].set_ylim((0,ymax[run]))
        np.savetxt(sampledir + '/' + run + '.txt', np.asarray(results))
        n=n+1

    ax43.set_ylabel('Bubble fraction in frame')
    ax45.set_xlabel('Time (s)')
    ax46.set_xlabel('Time (s)')
    #plt.xscale('log')
    ax41.set_ylim([0.00, 0.02])
    ax42.set_ylim([0.00, 0.008])
    ax43.set_ylim([0.00, 0.01])
    ax44.set_ylim([0.00, 0.004])
    ax45.set_ylim([0.00, 0.005])
    ax46.set_ylim([0.00, 0.002])

    for ax in fig4.axes:
        ax.set_xlim=([0.0,1300])
    fig4.savefig(sampledir + 'combined.svg', transparent=True)


##############################################################################
##############################################################################
#                               Plotting Only
##############################################################################
##############################################################################

runlist = [
           'start250', 'decay250',
           'start100', 'decay100',
           'start50', 'decay50',
           ]

ymax = {'start250':0.03,
        'decay250':0.03,
        'start100':0.03,
        'decay100':0.03,
        'start50':0.03,
        'decay50':0.03}

dtype = [('time', float), ('blacklevel', float), ('stamp', float)]
for sample in samples.keys():
    sampledir = rootdir + sample + '/'
    fig5 = plt.figure(constrained_layout=True, figsize=(7, 9))
    spec5 = gridspec.GridSpec(ncols=2, nrows=3, figure=fig5)
    ax51 = fig5.add_subplot(spec5[0, 0])
    ax52 = fig5.add_subplot(spec5[0, 1])
    ax53 = fig5.add_subplot(spec5[1, 0])
    ax54 = fig5.add_subplot(spec5[1, 1])
    ax55 = fig5.add_subplot(spec5[2, 0])
    ax56 = fig5.add_subplot(spec5[2, 1])
    n = 0
    for run in runlist:
        if 'start' in run:
            color = ['#ff7373','#ff1717', '#ba0000', '#5d0000']
        else:
            color = ['#73a9cd', '#1771ac', '#004978', '#004069']
        results = list(np.loadtxt(sampledir + run + '.txt'))
        results.sort(key=lambda x: int(x[2]))
        results = np.asarray(results)
        results1 = np.split(results,
                            np.where(np.gradient(results[:,0]) <=0)[0][1::2])
        m = 0
        for data in results1:
            if len(data) <= 5:
                print('array too short...')
            else:
                fig5.axes[n].scatter(data[:,0],
                                     data[:,1],
                                     color=color[m],
                                     alpha=0.2)
                fig5.axes[n].set_xlim((0,1300))
                fig5.axes[n].set_ylim((0,ymax[run]))
                m = m + 1
        n = n + 1
    fig5.suptitle(samples[sample][2])
    fig5.savefig(sampledir + 'combined2.svg', transparent=True)
    fig5


##############################################################################
##############################################################################
#                         Plotting + Processing
##############################################################################
##############################################################################

runlist = [
           'start250', 'decay250',
           'start100', 'decay100',
           'start50', 'decay50',
           ]

ymax = {'start250':0.03,
        'decay250':0.03,
        'start100':0.03,
        'decay100':0.03,
        'start50':0.03,
        'decay50':0.03}

dtype = [('time', float), ('blacklevel', float), ('stamp', float)]
for sample in samples.keys():
    sampledir = rootdir + sample + '/'
    fig5 = plt.figure(constrained_layout=True, figsize=(7, 9))
    spec5 = gridspec.GridSpec(ncols=2, nrows=3, figure=fig5)
    ax51 = fig5.add_subplot(spec5[0, 0])
    ax52 = fig5.add_subplot(spec5[0, 1])
    ax53 = fig5.add_subplot(spec5[1, 0])
    ax54 = fig5.add_subplot(spec5[1, 1])
    ax55 = fig5.add_subplot(spec5[2, 0])
    ax56 = fig5.add_subplot(spec5[2, 1])
    n = 0
    for run in runlist:
        if 'start' in run:
            color = ['#ff7373','#ff1717', '#ba0000', '#5d0000']
        else:
            color = ['#73a9cd', '#1771ac', '#004978', '#004069']
        results = list(np.loadtxt(sampledir + run + '.txt'))
        results.sort(key=lambda x: int(x[0]))
        results = np.asarray(results)
        np.split()
        results1 = np.split(results, np.where(results[:,0] > 250)[0][0:1])
        bins1 = np.linspace(results1[0][0,0], results1[0][-1,0], 50)
        bins2 = np.linspace(results1[1][0,0], results1[1][-1,0], 50)
        digitized = np.digitize(results1[0], bins1)
        bin_means = [data[digitized == i].mean() for i in range(1, len(bins))]

    fig5.suptitle(samples[sample][2])
    fig5.savefig(sampledir + 'combined2.svg', transparent=True)
    fig5
