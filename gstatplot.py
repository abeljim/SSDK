#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:01:15 2018

@author: mcdevitt
"""


import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import signal
import mdat2 as mdat

from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as mticker
from matplotlib.patches import Polygon
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection



def make_box(ax, xdata, ydata, width, height, facecolor='r', edgecolor='None', alpha=0.5):

    # Create list for all the error patches
    boxes = []
    
    if xdata.dtype == 'float64':
        rect = Rectangle((xdata, ydata), width, height)
        boxes.append(rect)
        
    # Loop over data points; create box from errors at each point
    else:    
        for x, y, xe, ye in zip(xdata, ydata, width.T, height.T):
            rect = Rectangle((x - xe[0], y - ye[0]), xe.sum(), ye.sum())
            boxes.append(rect)

    # Create patch collection with specified colour/alpha
    pc = PatchCollection(boxes, facecolor=facecolor, alpha=alpha,
                         edgecolor=edgecolor)

    # Add collection to axes
    ax.add_collection(pc)

    # Plot errorbars
    artists = ax.errorbar(xdata, ydata, xerr=width, yerr=height,
                          fmt='None', ecolor='k', alpha=0)

    return artists

def autolabel(rects, color):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        label = data_dict[next(key for key, value in tafelvalue.items() if value == rect.get_height())]
        plt.text(rect.get_x() + rect.get_width()/2., 0.5*height,
                label,
                ha='center', va='center',
                color = color,
                rotation='vertical'
                )

def decayfxn4(x, b, m, m2, t):
    return b+m*np.log10(x)+m2*(1-np.exp(-t*x))

def decayfxn5(x, b1, b2, m1, m2, t): 
    y = np.piecewise(x, [x < t, x >= t],
                     [lambda x:b1+m1*np.log10(x), lambda x:b2+m2*np.log10(x)])
    return y

def tafeleq(x, A, io):
    return io + (A * np.log(x))

wdir = "C:/Users/MummLab/Sierra/"

data_dict = {'10-8-18_bijel11_overpotential.mdat':'∞',
              #'9-28-18_scratches3_planar_overpotential.mdat':'∞',
             # '9-28-18_hp_planar_overpotential.mdat':'∞',
              }

tafelstdev = {}
tafelvalue = {}
slopes = {}
results = np.array(('File Name',
                    'Pore Size',
                    'eta1 10mA,cm2',
                    'eta2 10mA,cm2',
                    'eta1 20mA,cm2',
                    'eta2 20mA,cm2',
                    'eta1 30mA,cm2',
                    'eta2 30mA,cm2',
                    'Tafel Slope',
                    'Tafel Uncertainty'),
                    ndmin=2)

bigtafelplot, (tafelax2) = plt.subplots(figsize=(6, 10))

tafelax2.set_xscale('log')    
tafelax2.xaxis.set_minor_formatter(mticker.FormatStrFormatter('%.2g'))
tafelax2.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.2g'))
tafelax2.ticklabel_format(format='plain')
tafelax2.set_ylabel('Overpotential, $\eta$ (mV)', fontproperties=mdat.font)
tafelax2.set_xlabel('Current density, $j$, ($mA/cm^2$)', fontproperties=mdat.font)

samplecount = {'powder':0,
               'bijel':0,
               'planar':0,
               }

for file_name in data_dict.keys():
    gstatplot, (gstatax1) = plt.subplots(figsize=(2.5, 3))
    gstatplot.tight_layout(pad=2.0, w_pad=1.0, h_pad=1.0)
    gstatax1.set_xscale('log')
    gstatax1.set_ylabel('Overpotential, $\eta$ (mV)', fontproperties=mdat.font)
    gstatax1.set_xlabel('Time, $t$, (s)', fontproperties=mdat.font)
    gstatax1.ticklabel_format(format='plain')
    gstatplot.suptitle(str(file_name))
    results1 = [file_name, data_dict[file_name]]
    print('Loading ' + file_name)
    if 'planar' in file_name:
          sampletype = 'planar'
    elif 'powder' in file_name:
          sampletype = 'powder'
    elif 'bijel' in file_name:
          sampletype = 'bijel'
    file_path= str(wdir + file_name)
    run, runlist = mdat.importdata(file_path)
    tafel = []
    for key in run:
        
        data = np.array(run[key])
        rate = int(len(data) // (data [-1,0] - data[0,0])) # measurement freq
        window = rate//100
        if window//2 == window/2:
            window = window+1
        if window == 1:
            window = 3
        
        # Define a data array in the runlist
        gradient = np.gradient(scipy.signal.savgol_filter(data[:,1], window*3 ,2))
        gradient = scipy.signal.savgol_filter(gradient, window, 2)
        gradient[gradient>0.15*np.amin(gradient)] = 0
        len(scipy.signal.argrelextrema(gradient, np.less)[0])
        # Find the regions where the device is in operation
        """
        if 'acid' in file_name:
            data = data[np.where(data[:,1] <= -0.05)[0]]
        else:
            data = data[np.where(np.gradient(data[:,1]) == np.amin(np.gradient(data[:,1])))[0][0]:]
            #data = data[np.where(data[:,1] <= -1.2)[0]]
        """
        # Split the array into regions of "on" and make a list of these data
        #onlist = np.split(data, (np.where(np.gradient(data[:,0]) >=1)[0]))
        onlist = np.split(data, scipy.signal.argrelextrema(gradient, np.less)[0])
        onlist.pop(0)
        if file_name == '9-20-18_bijel#9_overpotential.mdat':
           del onlist[-1]
        onlist = [i for i in onlist if len(i) >= 1000]
        onlist = [i for i in onlist if i[0,1] >= i[900,1]]
        del onlist[0]
        # plot the overpotential for gas evolution
        iparams = []
        iiparams = []
        times = []
        mineta = []
        maxeta = []
        f1, (ax1) = plt.subplots(1, 1)
        f1.set_size_inches(6, 4)
        #f2, (ax1, ax2) = plt.subplots(1, 2, sharey=False, sharex=False)
        #f2.set_size_inches(6, 4)
        ax1.set_ylabel('Overpotential $\eta$ (mV)', fontproperties=mdat.font)
        ax1.set_xlabel('Time (s)', fontproperties=mdat.font)

        n = 0
        for i in onlist:                
            print('Measuring run %i' % (n))
            nullpts = []
            tempi = np.array(i) # Copy the array to a temporary one
            
            tempi = tempi[:-30]
            # convert E (V) to overpotential (mV)
            if 'acid' in file_name:
                tempi[:,1] =  -1000 * (tempi[:,1] - mdat.h2_e_acid)
            else:
                tempi[:,1] =  -1000 * (tempi[:,1] - mdat.h2_e)
            
            # normalize the times - start all the gstat steps at T = 0
            # Nota bene, a T=0 will not plot well on a log scale.
            tempi[:,0] = tempi[:,0] - np.amin(tempi[:,0])
            tempi = tempi[np.where(tempi[:,0] < 10)]
            tempi = tempi[:-10]
            
            """
            There exist regions where the data is too noisy or not repeatable.
            These indices are identified in a list nullpts and everything up to
            the maximum index is removed.
            """
            # eliminate values where j is changing significantly
            try:
                nullpts.append(np.where(np.abs(np.gradient(tempi[:,2])) <= 0.0000000025)[0][0])
            except:
                print('Stable current for run %i' % (n))
            # Sometimes there is a dip in the beginning while the potentiostat
            # is settling in, usually below 0.01 seconds.  This line
            # removes these data
            #nullpts.append(np.amin(scipy.signal.argrelmax(tempi[:,1])))
            #nullpts.append(scipy.signal.argrelmin(scipy.signal.savgol_filter(tempi[1:-1,1], window, 2))[0][3])
            #nullpts.append(np.where(np.gradient(tempi[:,1]) == np.amin(np.gradient(tempi[:,1])))[0][0])
            #nullpts = np.sort(np.ndarray.flatten(np.asarray(nullpts)))
            # Don't delete any data after t = 1. Remove the last bits of the array
            while tempi[nullpts[-1],0] >= 1:
                nullpts = nullpts[:-1]
        
            if key == 'Step1':
                j = '10'
            elif key == 'Step2':
                j = '20'
            elif key == 'Step3':
                j = '30'
            
            # plot these on ax1 and eliminate the first few data 
            # points (at least T=0)
            ax1.semilogx(tempi[1:-30,0],
                         scipy.signal.savgol_filter(tempi[1:-30,1],
                                                    window, 2),
                         alpha=mdat.alpha,
                         color=mdat.gstatcolors2[j][n])
            
            gstatax1.semilogx(tempi[1:-30,0],
                              scipy.signal.savgol_filter(tempi[1:-30,1],
                                                         window, 2),
                              alpha=mdat.alpha,
                              color=mdat.gstatcolors2[j][n])
            # if the maximum point isn't too far into the experiment:
            tempi = tempi[nullpts[-1]:]
            #tempi = tempi[np.where(tempi[:-1,1] == np.amin(tempi[:-1,1]))[0][0]:]
            #if file_name in kiethleylist:
             #   tempi = tempi[:-3]
              #  tempi[:,1] =  scipy.signal.savgol_filter(tempi[:,1], 51, 2)
            
            # Append data to lists that we will average at the end of the loop
            maxeta.append(np.amax(tempi[:,1]))
            mineta.append(np.amin(tempi[1:,1]))
            tafel.append((j, np.amax(tempi[:,1])))
            
            n = n+1
            
        # Find the average minimum and maximum overpotential that are typical
        # in the plots.  Add these observations as text to the image.
        mineta = np.mean(np.asarray(mineta))
        maxeta = np.mean(np.asarray(maxeta))
        results1.append(mineta)
        results1.append(maxeta)
        textj = j + ' mA/cm2\n'
        text = 'Early overpotential:\n%.3g mV\nLate overpotential:\n%.3g mV\n$\Delta\eta$ = %.3g mV' % (mineta, maxeta, maxeta - mineta)
        ax1.text(0.02,0.98,
                 text,
                 horizontalalignment='left',
                 verticalalignment='top',
                 fontproperties=mdat.font,
                 transform=ax1.transAxes)
        
        # Draw a rectangle on the first plot that shows the span and range of
        # the second
        limits = plt.axis()
        
        # Finally, plot and save the data
        f1.suptitle(str(file_name) + ' - ' + textj)
        f1.savefig(mdat.tmpdir + file_name[:-5] + '_gstat' + j + 'mA.svg', transparent=True)
        plt.close(f1)
        
    gstatplot.savefig(mdat.tmpdir + file_name[:-5] + '_gstat.svg', transparent=True)
    plt.close(gstatplot)
    # Find the Tafel slope from this galvanostatic data
    tafelplot, (tafelax1) = plt.subplots(1, 1)
    tafelplot.set_size_inches(4, 4)
#    tafelplot.tight_layout()
    tafelplot.suptitle(file_name + ' - Tafel')
    tafel = np.asarray(tafel, dtype=float)
    tafelfit = scipy.optimize.curve_fit(tafeleq, tafel[:,0], tafel[:,1])
    tafelvalue[file_name] = tafelfit[0][0]
    tafelstdev[file_name] = np.sqrt(np.diag(tafelfit[1]))[0]
    tafeltext = '%.3g +/- %.2g mV/dec' % (tafelfit[0][0],
                                          tafelstdev[file_name])
    results1.append(tafelvalue[file_name])
    results1.append(tafelstdev[file_name])
    
    vertices = [[(np.amin(tafel[:,0])),
                 (np.amax(tafel[:,0])),
                 (np.amax(tafel[:,0])),
                 (np.amin(tafel[:,0]))],
                [tafeleq(np.amin(tafel[:,0]),
                         tafelfit[0][0]+tafelstdev[file_name],
                         tafelfit[0][1]+np.sqrt(np.diag(tafelfit[1]))[1]),
                 tafeleq(np.amax(tafel[:,0]),
                         tafelfit[0][0]+tafelstdev[file_name],
                         tafelfit[0][1]+np.sqrt(np.diag(tafelfit[1]))[1]),
                 tafeleq(np.amax(tafel[:,0]),
                         tafelfit[0][0]-tafelstdev[file_name],
                         tafelfit[0][1]-np.sqrt(np.diag(tafelfit[1]))[1]),
                 tafeleq(np.amin(tafel[:,0]),
                         tafelfit[0][0]-tafelstdev[file_name],
                         tafelfit[0][1]-np.sqrt(np.diag(tafelfit[1]))[1])
                 ]]
                 
    polygon1 = Polygon(np.array(vertices).T,
                       facecolor='black',
                       alpha = 0.1)
    tafelax1.add_patch(polygon1)
    polygon2 = Polygon(np.array(vertices).T,
                       facecolor=mdat.typecolors[sampletype][samplecount[sampletype]],
                       alpha = 0.1)
    tafelax2.add_patch(polygon2)
    
    spots = 0
    if spots == 1:
        tafelax1.scatter(tafel[np.where(tafel[:,0] == 10),0],
                         tafel[np.where(tafel[:,0] == 10),1],
                         color=mdat.gstatcolors2['10'][5],
                         alpha = mdat.alpha)
        tafelax1.scatter(tafel[np.where(tafel[:,0] == 20),0],
                         tafel[np.where(tafel[:,0] == 20),1],
                         color=mdat.gstatcolors2['20'][5],
                         alpha = mdat.alpha)
        tafelax1.scatter(tafel[np.where(tafel[:,0] == 30),0],
                         tafel[np.where(tafel[:,0] == 30),1],
                         color=mdat.gstatcolors2['30'][5],
                         alpha = mdat.alpha)
        tafelax2.scatter(tafel[np.where(tafel[:,0] == 10),0],
                         tafel[np.where(tafel[:,0] == 10),1],
                         color=mdat.typecolors[sampletype][samplecount[sampletype]+5],
                         alpha = mdat.alpha)
        tafelax2.scatter(tafel[np.where(tafel[:,0] == 20),0],
                         tafel[np.where(tafel[:,0] == 20),1],
                         color=mdat.typecolors[sampletype][samplecount[sampletype]+5],
                         alpha = mdat.alpha)
        tafelax2.scatter(tafel[np.where(tafel[:,0] == 30),0],
                         tafel[np.where(tafel[:,0] == 30),1],
                         color=mdat.typecolors[sampletype][samplecount[sampletype]+5],
                         alpha = mdat.alpha)
    else:
        tafelax1.errorbar(np.mean(tafel[np.where(tafel[:,0] == 10),0]),
                          np.mean(tafel[np.where(tafel[:,0] == 10),1]),
                          color=mdat.gstatcolors2['10'][5],
                          fmt='o',
                          yerr=np.std(tafel[np.where(tafel[:,0] == 10),1]),
                          ecolor='black',
                          alpha = 0.5)
        tafelax1.errorbar(np.mean(tafel[np.where(tafel[:,0] == 20),0]),
                          np.mean(tafel[np.where(tafel[:,0] == 20),1]),
                          color=mdat.gstatcolors2['20'][5],
                          fmt='o',
                          yerr=np.std(tafel[np.where(tafel[:,0] == 20),1]),
                          ecolor='black',
                          alpha = 0.5)
        tafelax1.errorbar(np.mean(tafel[np.where(tafel[:,0] == 30),0]),
                          np.mean(tafel[np.where(tafel[:,0] == 30),1]),
                          color=mdat.gstatcolors2['30'][5],
                          fmt='o',
                          yerr=np.std(tafel[np.where(tafel[:,0] == 30),1]),
                          ecolor='black',
                          alpha = 0.5)
        tafelax2.errorbar(np.mean(tafel[np.where(tafel[:,0] == 10),0]),
                          np.mean(tafel[np.where(tafel[:,0] == 10),1]),
                          color=mdat.typecolors[sampletype][samplecount[sampletype]+5],
                          fmt='o',
                          yerr=np.std(tafel[np.where(tafel[:,0] == 10),1]),
                          ecolor='black',
                          alpha = 0.5)
        tafelax2.errorbar(np.mean(tafel[np.where(tafel[:,0] == 20),0]),
                          np.mean(tafel[np.where(tafel[:,0] == 20),1]),
                          color=mdat.typecolors[sampletype][samplecount[sampletype]+5],
                          fmt='o',
                          yerr=np.std(tafel[np.where(tafel[:,0] == 20),1]),
                          ecolor='black',
                          alpha = 0.5)
        tafelax2.errorbar(np.mean(tafel[np.where(tafel[:,0] == 30),0]),
                          np.mean(tafel[np.where(tafel[:,0] == 30),1]),
                          color=mdat.typecolors[sampletype][samplecount[sampletype]+5],
                          fmt='o',
                          yerr=np.std(tafel[np.where(tafel[:,0] == 30),1]),
                          ecolor='black',
                          alpha = 0.5)
            
        tafelax1.plot(np.array([np.amin(tafel[:,0]),
                                np.amax(tafel[:,0])
                                ]),
                      np.array([tafeleq(np.amin(tafel[:,0]),
                                        tafelfit[0][0],
                                        tafelfit[0][1]),
                                tafeleq(np.amax(tafel[:,0]),
                                        tafelfit[0][0],
                                        tafelfit[0][1])
                                ]),
                      color = 'black')
        tafelax2.plot(np.array([np.amin(tafel[:,0]),
                                np.amax(tafel[:,0])
                                ]),
                      np.array([tafeleq(np.amin(tafel[:,0]),
                                        tafelfit[0][0],
                                        tafelfit[0][1]),
                                tafeleq(np.amax(tafel[:,0]),
                                        tafelfit[0][0],
                                        tafelfit[0][1])
                                ]),
                      color = mdat.typecolors[sampletype][samplecount[sampletype]+5])

        #plt.gcf().gca().add_artist(polygon)
        
    tafelax1.set_xscale('log')    
    tafelax1.xaxis.set_minor_formatter(mticker.FormatStrFormatter('%.2g'))
    tafelax1.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.2g'))
    tafelax1.ticklabel_format(format='plain')
    tafelax1.set_ylabel('Overpotential, $\eta$ (mV)', fontproperties=mdat.font)
    tafelax1.set_xlabel('Current density, $j$, ($mA/cm^2$)', fontproperties=mdat.font)

    tafelax1.text(0.02,0.98,
                  'Tafel slope:  ' + tafeltext,
                  horizontalalignment='left',
                  verticalalignment='top',
                  fontproperties=mdat.font,
                  transform=tafelax1.transAxes)
    tafelplot.subplots_adjust(top=0.9)
    #plt.show(tafelplot)    
    tafelplot.savefig(mdat.tmpdir + file_name[:-5] + '_gstat_tafel.svg', transparent=True)
    plt.close(tafelplot)
    results = np.concatenate((results, np.array(results1, ndmin=2)))
    samplecount[sampletype] = samplecount[sampletype] + 1
    
gstatplot