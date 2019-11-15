# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 18:23:59 2019

@author: MummLab
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
rootdir = '/tmp/decaycapture/'
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
            'bar':([1400,3400,670,2495], 170, 'Straight bar')
            'bar2':([1400,3400,670,2495], 170, 'Straight bar')
           }

samples = {
           }

##############################################################################
##############################################################################
#                   Standard Calibration Section
##############################################################################
##############################################################################


for sample in standard.keys():
    runlist = [0, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    ME_fig, ax1 = plt.subplots()
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
            
        del filelist[-1]
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
            ax1.scatter(run, np.sum(len(np.where(thresh1 == 0)[0]))/area,
                            color='green',
                            alpha=0.05)
        #plt.imsave('/tmp/threshold.png', thresh1, cmap='gray')
        boxes.append(list(results1))
        ax2.scatter(np.arange(0, 500, 5), results1)
        ax2.set_ylim(0,0.05)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Black level in frame')
        fig.savefig(sampledir + str(run) + '_' + 'overtime.svg')
        
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
    
    ax1.boxplot(boxes,
                positions=runlist,
                widths = 10,
                showfliers = False,
                whis=[10,90])
    ax1.set_title(standard[sample][2] + ' (Standard)')
    ax1.set_xlabel('Current ($\mu$A)')
    ax1.set_ylabel('Black level in frame')
    ax1.set_ylim([-0.0001, 0.03])
    ax1.set_xlim([0, 600])
    ME_fig.savefig(sampledir + 'calibration.svg')