import numpy as np
from zipfile import ZipFile
import matplotlib.pyplot as plt
import scipy
from scipy import signal
import mdat



def plothot(i, run, steps, cvmin, cvmax, plotmin, plotmax, plot, alpha=1):
    sweeprate = steps[i]
    # Create a dummy array onto which we can append data
    buffer = [run[s] for s in run.keys() if i in s][0][0:1]
    # In the dictionary Run01, there are steps that are named (Step01, etc)
    # similarly to the step that was identified as having a sweep rate of 5
    # take these arrays and process them in the following loop
    for iv in [run[s] for s in run.keys() if i in s]:
#        iv[:,2] = iv[:,2] * 1000    # Convert A to mA
        iv = iv[np.where(iv[:,1] > plotmin)]
        iv = iv[np.where(iv[:,1] < plotmax)]
        buffer = np.concatenate((buffer, iv))
        plot.plot(iv[:,1],
                  scipy.signal.savgol_filter(iv[:,2], 7, 2)*1000,
                  mdat.colors1[steps[i]],
                  alpha=alpha)
    iv = iv[:,1:3]
    iv = iv[np.where(iv[:,0] > cvmin)]
    iv = iv[np.where(iv[:,0] < cvmax)]
#    if len(buffer) >= 2:
    buffer = buffer[1:]
    buffer = buffer[np.where(buffer[:,1] > cvmin)]
    buffer = buffer[np.where(buffer[:,1] < cvmax)]
    potmax = np.nan
    try:
        if buffer[0,1] > buffer[-1,1]:  # A 'true' here indicates sweep down
            potmax = buffer[np.where(buffer[:,2] == np.amin(buffer[:,2]))][0][1]
            imax = np.mean(buffer[np.where(np.abs(buffer[:,1]-potmax) <= 0.005)][:,2])
            return potmax, imax*1000, sweeprate
        elif buffer[0,1] < buffer[-1,1]:    # A 'true' here indicates sweep up
            potmax = buffer[np.where(buffer[:,2] == np.amax(buffer[:,2]))][0][1]
            imax = np.mean(buffer[np.where(np.abs(buffer[:,1]-potmax) <= 0.005)][:,2])
            return potmax, imax*1000, sweeprate
    except:
        return buffer
#### #### #### #### #### #### Set variables for the program here
wdir = "C:/Users/MummLab/Sierra/CV/"
file_names = [
              '6-21-18_ME.mdat',
              '7-26-18_planar_pellet_CV.mdat',
              '7-16-18_P_powder_CV.mdat',
              '8-14-18_bijel#10_CV.zip',
              '7-26-18_planar_bijels_CV.zip'
              ]



    
#### #### #### #### #### #### Start the program


figure, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3))
ax1.set_yticklabels([])
ax2.set_yticklabels([])
ax3.set_yticklabels([])
plotmin, plotmax = -0.5, 0.8   # Set the limits for the plot here


results = np.asarray([['data'], [5],[-5],[10],[-10],[25],[-25],[50],[-50],[100],[-100],[250],[-250]])
"""




"""
file_path= str(wdir + file_names[0])
run, runlist = mdat.importdata(file_path)
steps = {}  # make a dictionary with steps and sweep rates
for line in runlist:
        if line.startswith(b'Potentiodynamic'):
            steps[str(line)[str(line).find("Step"):str(line).find("Step")+6]] = str(line)[str(line).find(",", str(line).find("mV/S")-5, str(line).find("mV/S"))+1:str(line).find("mV/S")]
try:
    del steps['Step02'] # remove the first (Step02) wchich is technically potentiodynamic but not the CV section
except:
    print('No Step02!')

sweeps = []

if 'ME' in file_names[0]:
    cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
elif 'MicroElec' in file_names[0]:
    cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
elif '#' in file_names[0]:
    cvmin, cvmax = -0.2, 0.55      # Set the limits for the duck curve here
elif 'powder' in file_names[0]:
    cvmin, cvmax = -0.2, 0.8       # Set the limits for the duck curve here
elif 'med' in file_names[0]:
    cvmin, cvmax = 0.2, 0.6       # Set the limits for the duck curve here
elif 'planar' in file_names[0]:
    cvmin, cvmax = 0.2, 0.6       # Set the limits for the duck curve here


# For every named step in the steps dictionary (Step01, Step02, etc)
for i in steps.keys():
    #print(i)
    
    """
    Cathodic peaks are simple to find, but the anodic peaks can be convoluted
    by gas evolution.  Use these peaks for SA with caution!  Because of this
    convolution, the peaks must be selected by finding either where the first
    derivative makes a minima, or where the second derivative crosses the x axis
    """
    sweep = run[i + '_Rp01'][:,1:3]
    # first derivative
    sweep = np.concatenate((run[i + '_Rp01'][:,1:3], np.zeros((len(sweep),1))), axis=1)
    sweep[:,1] = scipy.signal.savgol_filter(sweep[:,1], 71, 2)
    for i_n in np.arange(5,len(sweep)-5):
        sweep[i_n, 2] = (sweep[i_n+5,1] - sweep[i_n-5,1]) /  (sweep[i_n+5,0] - sweep[i_n-5,0])
    sweep = sweep[10:-10]
    sweep[:,2] = scipy.signal.savgol_filter(sweep[:,2], 71, 2)
    
    # second derivative
    sweep = np.concatenate((sweep, np.zeros((len(sweep),1))), axis=1)
    for i_n in np.arange(1,len(sweep)-1):
        sweep[i_n, 3] = (sweep[i_n+1,2] - sweep[i_n-1,2]) /  (sweep[i_n+1,0] - sweep[i_n-1,0])
    sweep = sweep[1:-1]
    
    sweep[:,3] = scipy.signal.savgol_filter(sweep[:,3], 51, 3)
    sweep = sweep[np.where(sweep[:,0] >= 0.4)]
    
    if sweep[0,0] <= sweep[-1,0]:
        n = len(sweep) - 1 
        if sweep[np.where(sweep[:,1] == np.amin(sweep[:,1])),0][0][0] >= cvmax:
            cvmax1 = sweep[np.where(sweep[:,1] == np.amin(sweep[:,1])),0][0][0]
        
        elif sweep[np.where(sweep[:,2] == np.amin(sweep[:,2])),0][0][0] >= 0.4:
            cvmax1 = sweep[np.where(sweep[:,2] == np.amin(sweep[:,2])),0][0][0]
        else:
            cvmax1 = sweep[np.where(((np.roll(np.sign(sweep[:,3]), 1) - np.sign(sweep[:,3])) != 0).astype(int) == 1)[0][-1]][0]
        cvmin1 = cvmin
    else:
        cvmin1, cvmax1 = cvmin, cvmax

    point = plothot(i, run, steps, cvmin1, cvmax1, plotmin, plotmax, ax1, mdat.alpha)
    try: 
        ax1.scatter(point[0],
                    point[1],
                    s=150,
                    c=mdat.colors3[point[2]],
                    zorder=4)
        point = np.asarray(point)
        sweeps.append(point)
        point[2] = float(point[2])
        #ax1.ylabel('Current (mA)', fontproperties=mdat.font)
        ax1.xlabel('Potential (V) vs Ag/AgCl (1M KCl)', fontproperties=mdat.font)
    except:
        print('    No peak for ' + i)    
dlayer_cap = np.asarray(sweeps, dtype=float)
dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] = dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] * -1
cathodic = np.asarray([point for point in dlayer_cap if float(point[1]) <= 0])
anodic = np.asarray([point for point in dlayer_cap if float(point[1]) >= 0])
ax1.set_ylim([1.1 * cathodic[-1,1], 1.1 * anodic[-1,1]])

"""


"""


file_path= str(wdir + file_names[1])
run, runlist = mdat.importdata(file_path)
steps = {}  # make a dictionary with steps and sweep rates
for line in runlist:
        if line.startswith(b'Potentiodynamic'):
            steps[str(line)[str(line).find("Step"):str(line).find("Step")+6]] = str(line)[str(line).find(",", str(line).find("mV/S")-5, str(line).find("mV/S"))+1:str(line).find("mV/S")]
try:
    del steps['Step02'] # remove the first (Step02) wchich is technically potentiodynamic but not the CV section
except:
    print('No Step02!')

sweeps = []

if 'ME' in file_names[1]:
    cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
elif 'MicroElec' in file_names[1]:
    cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
elif '#' in file_names[1]:
    cvmin, cvmax = -0.2, 0.55      # Set the limits for the duck curve here
elif 'powder' in file_names[1]:
    cvmin, cvmax = -0.2, 0.8       # Set the limits for the duck curve here
elif 'med' in file_names[1]:
    cvmin, cvmax = 0.2, 0.6       # Set the limits for the duck curve here
elif 'planar' in file_names[1]:
    cvmin, cvmax = 0.2, 0.6       # Set the limits for the duck curve here


# For every named step in the steps dictionary (Step01, Step02, etc)
for i in steps.keys():
    #print(i)
    
    """
    Cathodic peaks are simple to find, but the anodic peaks can be convoluted
    by gas evolution.  Use these peaks for SA with caution!  Because of this
    convolution, the peaks must be selected by finding either where the first
    derivative makes a minima, or where the second derivative crosses the x axis
    """
    sweep = run[i + '_Rp01'][:,1:3]
    # first derivative
    sweep = np.concatenate((run[i + '_Rp01'][:,1:3], np.zeros((len(sweep),1))), axis=1)
    sweep[:,1] = scipy.signal.savgol_filter(sweep[:,1], 71, 2)
    for i_n in np.arange(5,len(sweep)-5):
        sweep[i_n, 2] = (sweep[i_n+5,1] - sweep[i_n-5,1]) /  (sweep[i_n+5,0] - sweep[i_n-5,0])
    sweep = sweep[10:-10]
    sweep[:,2] = scipy.signal.savgol_filter(sweep[:,2], 71, 2)
    
    # second derivative
    sweep = np.concatenate((sweep, np.zeros((len(sweep),1))), axis=1)
    for i_n in np.arange(1,len(sweep)-1):
        sweep[i_n, 3] = (sweep[i_n+1,2] - sweep[i_n-1,2]) /  (sweep[i_n+1,0] - sweep[i_n-1,0])
    sweep = sweep[1:-1]
    
    sweep[:,3] = scipy.signal.savgol_filter(sweep[:,3], 51, 3)
    sweep = sweep[np.where(sweep[:,0] >= 0.4)]
    
    if sweep[0,0] <= sweep[-1,0]:
        n = len(sweep) - 1 
        if sweep[np.where(sweep[:,1] == np.amin(sweep[:,1])),0][0][0] >= cvmax:
            cvmax1 = sweep[np.where(sweep[:,1] == np.amin(sweep[:,1])),0][0][0]
        
        elif sweep[np.where(sweep[:,2] == np.amin(sweep[:,2])),0][0][0] >= 0.4:
            cvmax1 = sweep[np.where(sweep[:,2] == np.amin(sweep[:,2])),0][0][0]
        else:
            cvmax1 = sweep[np.where(((np.roll(np.sign(sweep[:,3]), 1) - np.sign(sweep[:,3])) != 0).astype(int) == 1)[0][-1]][0]
        cvmin1 = cvmin
    else:
        cvmin1, cvmax1 = cvmin, cvmax

    point = plothot(i, run, steps, cvmin1, cvmax1, plotmin, plotmax, ax2, mdat.alpha)
    try: 
        ax2.scatter(point[0],
                    point[1],
                    s=150,
                    c=mdat.colors3[point[2]],
                    zorder=4)
        point = np.asarray(point)
        sweeps.append(point)
        point[2] = float(point[2])
        #ax1.ylabel('Current (mA)', fontproperties=mdat.font)
        ax2.xlabel('Potential (V) vs Ag/AgCl (1M KCl)', fontproperties=mdat.font)
    except:
        print('    No peak for ' + i)
dlayer_cap = np.asarray(sweeps, dtype=float)
dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] = dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] * -1
cathodic = np.asarray([point for point in dlayer_cap if float(point[1]) <= 0])
anodic = np.asarray([point for point in dlayer_cap if float(point[1]) >= 0])

ax2.set_xlim(plotmin, plotmax)
ax2.set_ylim([1.1 * cathodic[-1,1], 1.1 * anodic[-1,1]])

"""





"""

file_path= str(wdir + file_names[2])
run, runlist = mdat.importdata(file_path)
steps = {}  # make a dictionary with steps and sweep rates
for line in runlist:
        if line.startswith(b'Potentiodynamic'):
            steps[str(line)[str(line).find("Step"):str(line).find("Step")+6]] = str(line)[str(line).find(",", str(line).find("mV/S")-5, str(line).find("mV/S"))+1:str(line).find("mV/S")]
try:
    del steps['Step02'] # remove the first (Step02) wchich is technically potentiodynamic but not the CV section
except:
    print('No Step02!')

sweeps = []

if 'ME' in file_names[2]:
    cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
elif 'MicroElec' in file_names[2]:
    cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
elif '#' in file_names[2]:
    cvmin, cvmax = -0.2, 0.55      # Set the limits for the duck curve here
elif 'powder' in file_names[2]:
    cvmin, cvmax = -0.2, 0.8       # Set the limits for the duck curve here
elif 'med' in file_names[2]:
    cvmin, cvmax = 0.2, 0.6       # Set the limits for the duck curve here
elif 'planar' in file_names[2]:
    cvmin, cvmax = 0.2, 0.6       # Set the limits for the duck curve here


# For every named step in the steps dictionary (Step01, Step02, etc)
for i in steps.keys():
    #print(i)
    
    """
    Cathodic peaks are simple to find, but the anodic peaks can be convoluted
    by gas evolution.  Use these peaks for SA with caution!  Because of this
    convolution, the peaks must be selected by finding either where the first
    derivative makes a minima, or where the second derivative crosses the x axis
    """
    sweep = run[i + '_Rp01'][:,1:3]
    # first derivative
    sweep = np.concatenate((run[i + '_Rp01'][:,1:3], np.zeros((len(sweep),1))), axis=1)
    sweep[:,1] = scipy.signal.savgol_filter(sweep[:,1], 71, 2)
    for i_n in np.arange(5,len(sweep)-5):
        sweep[i_n, 2] = (sweep[i_n+5,1] - sweep[i_n-5,1]) /  (sweep[i_n+5,0] - sweep[i_n-5,0])
    sweep = sweep[10:-10]
    sweep[:,2] = scipy.signal.savgol_filter(sweep[:,2], 71, 2)
    
    # second derivative
    sweep = np.concatenate((sweep, np.zeros((len(sweep),1))), axis=1)
    for i_n in np.arange(1,len(sweep)-1):
        sweep[i_n, 3] = (sweep[i_n+1,2] - sweep[i_n-1,2]) /  (sweep[i_n+1,0] - sweep[i_n-1,0])
    sweep = sweep[1:-1]
    
    sweep[:,3] = scipy.signal.savgol_filter(sweep[:,3], 51, 3)
    sweep = sweep[np.where(sweep[:,0] >= 0.4)]
    
    if sweep[0,0] <= sweep[-1,0]:
        n = len(sweep) - 1 
        if sweep[np.where(sweep[:,1] == np.amin(sweep[:,1])),0][0][0] >= cvmax:
            cvmax1 = sweep[np.where(sweep[:,1] == np.amin(sweep[:,1])),0][0][0]
        
        elif sweep[np.where(sweep[:,2] == np.amin(sweep[:,2])),0][0][0] >= 0.4:
            cvmax1 = sweep[np.where(sweep[:,2] == np.amin(sweep[:,2])),0][0][0]
        else:
            cvmax1 = sweep[np.where(((np.roll(np.sign(sweep[:,3]), 1) - np.sign(sweep[:,3])) != 0).astype(int) == 1)[0][-1]][0]
        cvmin1 = cvmin
    else:
        cvmin1, cvmax1 = cvmin, cvmax

    point = plothot(i, run, steps, cvmin1, cvmax1, plotmin, plotmax, ax3, mdat.alpha)
    try: 
        ax3.scatter(point[0],
                    point[1],
                    s=150,
                    c=mdat.colors3[point[2]],
                    zorder=4)
        point = np.asarray(point)
        sweeps.append(point)
        point[2] = float(point[2])
        #ax1.ylabel('Current (mA)', fontproperties=mdat.font)
        ax3.xlabel('Potential (V) vs Ag/AgCl (1M KCl)', fontproperties=mdat.font)
    except:
        print('    No peak for ' + i)    
dlayer_cap = np.asarray(sweeps, dtype=float)
dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] = dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] * -1
cathodic = np.asarray([point for point in dlayer_cap if float(point[1]) <= 0])
anodic = np.asarray([point for point in dlayer_cap if float(point[1]) >= 0])

ax3.set_ylim([1.1 * cathodic[-1,1], 1.1 * anodic[-1,1]])
