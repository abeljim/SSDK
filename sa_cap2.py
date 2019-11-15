import numpy as np
from zipfile import ZipFile
import matplotlib.pyplot as plt
import scipy
from scipy import signal
import mdat2 as mdat



def plothot(i, run, steps, cvmin, cvmax, plotmin, plotmax, alpha=1):
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
        plt.plot(iv[:,1],
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
#wdir = '/home/mcdevitt/Dropbox/UCI/Research/McDevitt Bijel Electrodes/Data/Electrochemical Data/oxygen evolution/surface area/'
file_names = [
#              '6-19-18_powder.mdat',
               '6-21-18_ME.mdat',
#              '6-25-18_ME_STIRRED.mdat',
#              '6-25-18_Powder_Stirred_2.mdat',
#              '6-7_Cyclical_MicroElec.mdat',
#              '6-7_Cyclical_bijel1_broken.mdat'
#              '6-19-18_Bijel.mdat',
#              '6-28-18_bijel stirred.mdat',
#              '6-29-18_sm_Powder_stirred.mdat',
#              '7-9-18_sm_powder_sonication.mdat',
#              '7-16-18_P_powder_CV.mdat',
#              '7-20_18_bijel_#1_CV.mdat', 
              '7-24-19_B15_CV.zip',
              '7-24-19_B17_CV.zip'
              ]

    
#### #### #### #### #### #### Start the program

results = np.asarray([['data'], [5],[-5],[10],[-10],[25],[-25],[50],[-50],[100],[-100],[250],[-250]])

for file_name in file_names:
    
    file_path= str(wdir + file_name)

    
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
    
    if 'ME' in file_name:
        cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
        plotmin, plotmax = 0.1, 0.5   # Set the limits for the plot here
    elif 'MicroElec' in file_name:
        cvmin, cvmax = 0.2, 0.4       # Set the limits for the duck curve here
        plotmin, plotmax = 0.1, 0.5   # Set the limits for the plot here
    elif 'Powder' in file_name:
        cvmin, cvmax = -0.2, 0.8       # Set the limits for the duck curve here
        plotmin, plotmax = -0.4, 0.8   # Set the limits for the plot here
    elif 'Bijel' or 'bijel' in file_name:
        cvmin, cvmax = -0.2, 0.55      # Set the limits for the duck curve here
        plotmin, plotmax = -0.4, 0.8   # Set the limits for the plot here
    
    
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
    
        point = plothot(i, run, steps, cvmin1, cvmax1, plotmin, plotmax, mdat.alpha)
        try: 
            plt.scatter(point[0],
                        point[1],
                        s=150,
                        c=mdat.colors3[point[2]],
                        zorder=4)
            point = np.asarray(point)
            sweeps.append(point)
            point[2] = float(point[2])
            plt.ylabel('Current (mA)', fontproperties=mdat.font)
            plt.xlabel('Potential (V) vs Ag/AgCl (1M KCl)', fontproperties=mdat.font)
        except:
            print('    No peak for ' + i)    
    dlayer_cap = np.asarray(sweeps, dtype=float)
    dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] = dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] * -1
    cathodic = np.asarray([point for point in dlayer_cap if float(point[1]) <= 0])
    anodic = np.asarray([point for point in dlayer_cap if float(point[1]) >= 0])
    cathodic = ''
    anodic = ''

    for point in [point for point in dlayer_cap if float(point[1]) <= 0]:
        cathodic = cathodic + '-%.3g mV/s, %.3g mA \n' % (point[2], point[1])
    for point in np.flip([point for point in dlayer_cap if float(point[1]) >= 0], axis=0):
        anodic = anodic + '%.3g mV/s, %.3g mA \n' % (point[2], point[1])

    anodic = anodic[:-1]
    cathodic = cathodic[:-1]
    
    plt.text(plotmin,
             np.amax(dlayer_cap[:,1]),
             anodic,
             horizontalalignment='left',
             verticalalignment='top',
             fontproperties=mdat.font)
    plt.text(plotmax,
             np.amin(dlayer_cap[:,1]),
             cathodic,
             horizontalalignment='right',
             verticalalignment='bottom',
             fontproperties=mdat.font)
    plt.title(file_name, fontproperties=mdat.font)
#    plt.show()
    plt.savefig(mdat.tmpdir + file_name[:-5] + '_CV.svg', transparent=True, )
    plt.close()
    dlayer_cap[np.where(dlayer_cap[:,1] < 0),2] = dlayer_cap[np.where(dlayer_cap[:,1] < 0),2] * -1
    dlayer_cap = np.concatenate((np.array([['Peak E', 'Peak I', file_name]]), dlayer_cap))
    while len(dlayer_cap) < len(results):
        dlayer_cap = np.concatenate((dlayer_cap, np.tile(np.nan, (1,dlayer_cap.shape[1]))))
    results = np.concatenate((results, dlayer_cap), axis=1)
    #del buffer, keepCurrentSet, steplist, indices, plotmin, plotmax
    #del cvmin, cvmax, i, n, point, sweeps

#wdir = '/home/mcdevitt/Dropbox/UCI/Research/McDevitt Bijel Electrodes/Data/Electrochemical Data/oxygen evolution/supporting data/'
wdir = "C:/Users/MummLab/Sierra/CV/"
file_names2 = [
               '10-4-18_bijels11_and_12_CV.mdat'
               ]

runs = []

bijel11run = {}
bijel12run = {}

file_path= str(wdir + file_names2[0])
run, runlist = mdat.importdata2(file_path)

bijel11 = [s for s in run.keys() if "bijel#11" in s]
bijel12 = [s for s in run.keys() if "bijel#11" not in s]
for key in bijel11:
    bijel11run[key[10:]] = run[key]
for key in bijel12:
    bijel12run[key[10:]] = run[key]
    
del(bijel11, bijel12, run, key)


indexn = 1
for run in [bijel11run, bijel12run]:
    file_path= str(wdir + file_name)
    steps = {}  # make a dictionary with steps and sweep rates
    for line in runlist:
            if line.startswith(b'Potentiodynamic'):
                steps[str(line)[str(line).find("Step"):str(line).find("Step")+6]] = str(line)[str(line).find(",", str(line).find("mV/S")-5, str(line).find("mV/S"))+1:str(line).find("mV/S")]
    try:
        del steps['Step02'] # remove the first (Step02) wchich is technically potentiodynamic but not the CV section
    except:
        print('No Step02!')
    
    sweeps = []
    

    cvmin, cvmax = -0.2, 0.55      # Set the limits for the duck curve here
    plotmin, plotmax = -0.4, 0.8   # Set the limits for the plot here
    
    
    
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
    
        point = plothot(i, run, steps, cvmin1, cvmax1, plotmin, plotmax, mdat.alpha)
        try: 
            plt.scatter(point[0],
                        point[1],
                        s=150,
                        c=mdat.colors3[point[2]],
                        zorder=4)
            point = np.asarray(point)
            sweeps.append(point)
            point[2] = float(point[2])
            plt.ylabel('Current (mA)', fontproperties=mdat.font)
            plt.xlabel('Potential (V) vs Ag/AgCl (1M KCl)', fontproperties=mdat.font)
        except:
            print('    No peak for ' + i)    
    dlayer_cap = np.asarray(sweeps, dtype=float)
    dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] = dlayer_cap[np.where(dlayer_cap[:,1] < 0)[0]][:,2] * -1
    cathodic = np.asarray([point for point in dlayer_cap if float(point[1]) <= 0])
    anodic = np.asarray([point for point in dlayer_cap if float(point[1]) >= 0])
    cathodic = ''
    anodic = ''

    for point in [point for point in dlayer_cap if float(point[1]) <= 0]:
        cathodic = cathodic + '-%.3g mV/s, %.3g mA \n' % (point[2], point[1])
    for point in np.flip([point for point in dlayer_cap if float(point[1]) >= 0], axis=0):
        anodic = anodic + '%.3g mV/s, %.3g mA \n' % (point[2], point[1])

    anodic = anodic[:-1]
    cathodic = cathodic[:-1]
    """
    plt.text(plotmin,
             np.amax(dlayer_cap[:,1]),
             anodic,
             horizontalalignment='left',
             verticalalignment='top',
             fontproperties=mdat.font)
    plt.text(plotmax,
             np.amin(dlayer_cap[:,1]),
             cathodic,
             horizontalalignment='right',
             verticalalignment='bottom',
             fontproperties=mdat.font)
    """
    plt.title('bijel_1' + str(indexn), fontproperties=mdat.font)
#    plt.show()
    plt.savefig(mdat.tmpdir + 'bijel_1' + str(indexn)  + '_CV.svg', transparent=True, )
    plt.close()
    dlayer_cap[np.where(dlayer_cap[:,1] < 0),2] = dlayer_cap[np.where(dlayer_cap[:,1] < 0),2] * -1
    dlayer_cap = np.concatenate((np.array([['Peak E', 'Peak I', file_name]]), dlayer_cap))
    while len(dlayer_cap) < len(results):
        dlayer_cap = np.concatenate((dlayer_cap, np.tile(np.nan, (1,dlayer_cap.shape[1]))))
        
    indexn = indexn+1
    
    results = np.concatenate((results, dlayer_cap), axis=1)
    #del buffer, keepCurrentSet, steplist, indices, plotmin, plotmax
    #del cvmin, cvmax, i, n, point, sweeps

results2 = np.array(results[1:], dtype=float)

n=2
for file_name in ['ME', 'bijel11', 'bijel12']:
    print(file_name + ' Surface Area: %.3g +/- %.3g cm^2' % (np.mean(0.0019635 * results2[:7,n] / results2[:7,2]),
                                                             np.std(0.0019635 * results2[:7,n] / results2[:7,2])))
    n = n+3
