# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 11:57:34 2018

@author: MummLab
"""

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

wdir = 'C:/Users/MummLab/Kyle/'

data_dict = {
###              '7-18-18_med_planar_overpotential.mdat':'∞',
###              '7-18-18_med_planar_overpotential_long.mdat':'∞',
###              '7-11-18_powder_overpotential.mdat':'?',
###              '7-15-18_sm_bijel_old_overpotential.mdat':'?',
###              '7-17-18_P_powder_overpotential.mdat':'5 μm',
#              '7-17-18_P_powder_overpotential_long.mdat':'5 μm',
###              '7-18-18_C_powder_overpotential.mdat':'15 μm',
#              '7-18-18_C_powder_overpotential_long.mdat':'12 μm',
###              '7-16-18_AR_powder_overpotential.mdat':'30 μm',
#              '7-17-18_AR_powder_overpotential_long.mdat':'20 μm',
##              '8-23-18_AR3_overpotential_reassembled.mdat':'20 μm',
##              '8-23-18_AR3_overpotential_long.mdat':'20 μm',
#              '7-20-18_bijel#1_overpotential_manual.mdat':'7 μm',      # med bijel#
#              '8-2-18_bijel#3_overpotential.mdat':'7 μm',              # med bijel
#              '8-15-18_bijel#9_overpotential_long.mdat':'15 μm',
#              '8-1-18_bijel#6_overpotential.mdat':'18 μm',               # sm bijel
#              '8-15-18_bijel#10_overpotential_long.mdat':'25 μm', #            '8-1-18_bijel#7_overpotential.mdat':'25 μm',              # sm bijel
#              '7-25-18_bijel#5_overpotential.mdat':'80 μm',             # lg bijel
#              '8-2-18_bijel#4_overpotential.mdat':'90 μm',              # lg bijel
#              '7-31-18_planar_pellet_overpotential.mdat':'∞',
#              '7-31-18_planar_bijels_overpotential.mdat':'∞',
#              '7-13-18_med_planar_overpotential.mdat':'∞',
##              '8-22-18_P_powder_overpotential long_acid.mdat':'5 μm',
##              '8-23-18_C1_overpotential_long_acid.mdat':'15 μm',
##              '8-23-18_AR3_overpotential_long_acid.mdat':'30 μm',
#              '8-14-18_ME_overpotential_long2.mdat':'∞',
##              '8-14-18_Pt_overpotential_long_KM.mdat':'∞',
##              '8-16-18_ME_overpotential_long_acid.mdat':'∞',
##              '8-20-18_Pt_overpotential_long_acid.mdat':'∞',
##              '8-28-18_P_powder_overpotential_long.mdat':'5 μm',
##                '9-20-18_bijel9_overpotential.mdat',
##                '9-20-18_bijel10_overpotential.mdat',
#              '10-2-18_planar_EN_overpotential_1.mdat':'∞',
#              '10-5-18_bijel12.mdat':'dont know lol'
#               '10-10-18_HP.mdat':'inf'
#               'scratch0.mdat':'inf',
#               'scratch1.mdat':'inf',
#               'scratch2.mdat':'inf',
#               'scratch3.mdat':'inf'
               'B12_no sonic.mdat':'?',
               'scratch2_supersonic_and_stirred.mdat':'inf'
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
        data = np.array(run[key])
        # Find the regions where the device is in operation
        if 'acid' in file_name:
            data = data[np.where(data[:,1] <= -0.05)[0]]
        else:
            data = data[np.where(data[:,1] <= -1.2)[0]]
        # Split the array into regions of "on" and make a list of these data
        onlist = np.split(data, (np.where(np.gradient(data[:,0]) >=1)[0]))
        # Do the same for off regions
        data = np.array(run[key])
        data = data[np.where(data[:,2] >= -0.005)[0]]
        offlist = np.split(data, (np.where(np.gradient(data[:,0]) >=1)[0]))
        
        # Remove data from these lits if they are only one element long...
        # There's probably a more elegant way to solve this with the initial
        # np.split command, but oh well...
        onlist = [i for i in onlist if len(i) != 1] 
        offlist = [i for i in offlist if len(i) >= rate * 0.5]
        del offlist[0]  # Remove the first recovery (It's just empty time)
        del onlist[0]   # Remove the first recovery (it's not representitive)


        # plot the overpotential for gas evolution
        iparams = []
        iiparams = []
        times = []
        mineta = []
        maxeta = []
        f1, (ax1, ax3) = plt.subplots(1, 2, sharey=False, sharex=False)
        f1.set_size_inches(6, 4)
        #f2, (ax1, ax2) = plt.subplots(1, 2, sharey=False, sharex=False)
        #f2.set_size_inches(6, 4)
        ax1.set_ylabel('Overpotential $\eta$ (mV)', fontproperties=mdat.font)
        ax1.set_xlabel('Time (s)', fontproperties=mdat.font)
        ax3.set_xlabel('Time (s)', fontproperties=mdat.font)

        n = 0
        for i in onlist:                
            print('Measuring run %i' % (n))
            nullpts = []
            tempi = np.array(i) # Copy the array to a temporary one
            
            tempi = tempi[:-3]
            # convert E (V) to overpotential (mV)
            if 'acid' in file_name:
                tempi[:,1] =  -1000 * (tempi[:,1] - mdat.h2_e_acid)
            else:
                tempi[:,1] =  -1000 * (tempi[:,1] - mdat.h2_e)
            
            # normalize the times - start all the gstat steps at T = 0
            # Nota bene, a T=0 will not plot well on a log scale.
            tempi[:,0] = tempi[:,0] - np.amin(tempi[:,0])
            tempi = tempi[np.where(tempi[:,0] < 10)]
            
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
            nullpts.append(np.amin(scipy.signal.argrelmax(tempi[:,1])))
            nullpts.append(scipy.signal.argrelmin(scipy.signal.savgol_filter(tempi[1:-1,1], window, 2))[0][3])
            nullpts.append(np.where(np.gradient(tempi[:,1]) == np.amin(np.gradient(tempi[:,1])))[0][0])
            nullpts = np.sort(np.ndarray.flatten(np.asarray(nullpts)))
            # Don't delete any data after t = 1. Remove the last bits of the array
            while tempi[nullpts[-1],0] >= 1:
                nullpts = nullpts[:-1]
            
            # If we're running the kiethley manually, we'll need to make
            # assumptions on the current density.  EDIT:  This is a more robust
            # way to ID regions anyway
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

            tempi = tempi[:-3]
            tempi[:,1] =  scipy.signal.savgol_filter(tempi[:,1], 51, 2)
            
            # Append data to lists that we will average at the end of the loop
            maxeta.append(np.amax(tempi[:,1]))
            mineta.append(np.amin(tempi[1:,1]))
            tafel.append((j, np.amax(tempi[:,1])))
            
            if tempi[np.where(tempi[:,1] == np.amin(tempi[1:,1]))[0][-1],0] <=5:
                tempi = tempi[np.where(tempi[:,1] == np.amin(tempi[1:,1]))[0][-1]:]
            
            # If there is a dropoff in the overpotential at the end of the
            # experiment, it's likely the current was turned off immediately
            # before the end.  These data should not be plotted.  Remove
            # everything after the maximum overpotential if it occurs after
            # nine seconds
            if tempi[np.where(tempi[:,1] == np.amax(tempi[:,1]))[0][0],0] > 9:
                tempi = tempi[:np.where(tempi[:,1] == np.amax(tempi[:,1]))[0][0]]

            # Finally, plot this processed data on ax3
            ax3.semilogx(tempi[1:-1,0],
                         scipy.signal.savgol_filter(tempi[1:-1,1], window, 2),
                         alpha=mdat.alpha,
                         color=mdat.gstatcolors2[j][n])
            
            """
            Let's try to identify the two regions of interest in the plot.
            First, the array 'tempi' will be sampled on a logarithmic scale,
            then a change in the gradient will be evaluated
            """
            if len(np.where(tempi[:,1] <= 0.05)[0]) != 0:
                tempi = tempi[np.where(tempi[:,1] <= 0.05)[0][-1]:]
            tempi = tempi[np.where(tempi[:,1] == np.amin(tempi[:,1]))[0][0]:]
            
            
            try:
                po = scipy.optimize.curve_fit(decayfxn5,
                                              tempi[3:-1,0],
                                              tempi[3:-1,1],
                                              ##sigma = 1/tempi[:,0][1:],
                                              p0=np.array([np.amin(tempi[3:-1,1]),
                                                           np.amin(tempi[3:-1,1]),
                                                           15,
                                                           15,
                                                           1
                                                           ])
                                              )[0]
                loops = 0
                while np.abs(po[4] - 10**np.divide((po[0]-po[1]),(po[3]-po[2]))) >= 0.01:
                    #print(loops)
                    if loops >= 500:
                        raise ValueError('Failed to fit a curve')
                    po[4] = 10**np.divide((po[0]-po[1]),(po[3]-po[2]))
                    po = scipy.optimize.curve_fit(decayfxn5,
                                                  tempi[3:-1,0],
                                                  tempi[3:-1,1],
                                                  ##sigma = 1/tempi[:,0][1:],
                                                  p0=np.array([po[0],
                                                               po[1],
                                                               po[2],
                                                               po[3],
                                                               po[4]
                                                               ])
                                                  )[0]
                    loops = loops + 1
                iparams.append(scipy.optimize.curve_fit(decayfxn5,
                                                        tempi[3:-1,0],
                                                        tempi[3:-1,1],
                                                        ##sigma = 1/tempi[:,0][1:],
                                                        p0=np.array([po[0],
                                                                     po[1],
                                                                     po[2],
                                                                     po[3],
                                                                     po[4]
                                                                     ]))[0])
                iiparams.append(scipy.optimize.curve_fit(decayfxn5,
                                                         tempi[3:-1,0],
                                                         tempi[3:-1,1],
                                                         ##sigma = 1/tempi[:,0][1:],
                                                         p0=np.array([po[0],
                                                                      po[1],
                                                                      po[2],
                                                                      po[3],
                                                                      po[4]
                                                                      ]))[1])
            except:
                print('Optimal Parameters Not Found!')

            n = n+1
        
        # The parameters that are fit through the data, average them and plot
        # the representitive lines on ax3
        iparams = np.array(iparams)
        iiparams = np.array(iiparams)
        iparams = np.mean(iparams, axis=0)
        slopes[str(file_name + '_' + j)] = iparams
        t = iparams[-1]
        ax3.plot(tempi[:,0],
                 decayfxn5(tempi[:,0], iparams[0], iparams[1], iparams[2], iparams[3], iparams[4]),
                 color='black')
        
        # Find the average minimum and maximum overpotential that are typical
        # in the plots.  Add these observations as text to the image.
        mineta = np.mean(np.asarray(mineta))
        maxeta = np.mean(np.asarray(maxeta))
        results1.append(mineta)
        results1.append(maxeta)
        textj = j + ' mA/cm2\n'
        text = 'Early overpotential:\n%.3g mV\nLate overpotential:\n%.3g mV\n$\Delta\eta$ = %.3g mV\n T=%.2g seconds' % (mineta, maxeta, maxeta - mineta, t)
        ax3.text(0.02,0.98,
                 text,
                 horizontalalignment='left',
                 verticalalignment='top',
                 fontproperties=mdat.font,
                 transform=ax3.transAxes)
        
        # Draw a rectangle on the first plot that shows the span and range of
        # the second
        limits = plt.axis()
        make_box(ax1,
                 plt.axis()[0],
                 plt.axis()[2],
                 plt.axis()[1] - plt.axis()[0],
                 plt.axis()[3] - plt.axis()[2],
                 facecolor='#B9B9B9',
                 edgecolor='None',
                 alpha=0.5)
        
        # Finally, plot and save the data
        f1.suptitle(str(file_name) + ' - ' + textj)
        f1.savefig(mdat.tmpdir + file_name[:-5] + '_gstat' + j + 'mA.svg', transparent=True)
        plt.close(f1)
        
    gstatplot.savefig(mdat.tmpdir + file_name[:-5] + '_gstat.svg', transparent=True)
    plt.show(gstatplot)
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
    


bigtafelplot.savefig(mdat.tmpdir + 'gstat_tafel.svg', transparent=True)
plt.close(bigtafelplot)
tafeltable = []
for key, value in tafelvalue.items():
    tafeltable.append([key, value])

tafeltable = np.asarray(tafeltable)
tafeltable = np.concatenate((tafeltable, np.array(np.zeros(len(tafeltable)), ndmin=2).T), axis=1)
for line in tafeltable:
    line[-1] = tafelstdev[line[0]]

objects = []
values = []
for line in tafeltable:
    if 'powder' in line[0]:
        objects.append(str(line[0]))
        values.append(line[1:])
values = np.array(values, dtype = float)
items = []
try:
    powders = plt.bar(objects,
                      values[:,0],
                      label = objects,
                      yerr = values[:,1],
                      color = mdat.typecolors['powder'][5])
    autolabel(powders, 'white')
except IndexError:
    print('No Powders in table')

objects = []
values = []
for line in tafeltable:
    if 'bijel#' in line[0]:
        objects.append(str(line[0]))
        values.append(line[1:])
values = np.array(values, dtype = float)
items = []
try:
    bijels = plt.bar(objects,
                     values[:,0],
                     label = objects,
                     yerr = values[:,1],
                     color = mdat.typecolors['bijel'][5])
    autolabel(bijels, 'black')
except IndexError:
    print('No Bijels in table')
    
values=[]
objects = []
for line in tafeltable:
    if 'planar' in line[0]:
        objects.append(str(line[0]))
        values.append(line[1:])
values = np.array(values, dtype = float)
try:
    planars = plt.bar(objects,
                      values[:,0],
                      label = objects,
                      yerr = values[:,1],
                      color = mdat.typecolors['planar'][5])
    autolabel(planars, 'white')
except IndexError:
    print('No Planars in Table')



plt.ylabel('Tafel Slope (mV/dec)')
plt.suptitle('Tafel Slope chart')
plt.xticks(rotation='vertical')
plt.savefig(mdat.tmpdir + 'gstat_tafelslopecompare.svg', transparent=True)

for line in slopes:
    print(line)
np.savetxt(mdat.tmpdir + 'results.csv', results, fmt='%s', delimiter=',')
