# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:35:47 2018

@author: MummLab
"""
import visa
import keithley
from time import perf_counter
from time import sleep
import numpy as np
import datetime
import matplotlib.pyplot as plt

def plotdata(data):
    x1 = np.array(data[:,0], dtype=float)
    y1 = np.array(data[:,1], dtype=float)
    y2 = np.array(data[:,2], dtype=float)
    y2 = y2 * 1000
    x2 = np.array(data[np.where(data[:,0] >= data[-1,0]-3600),0]).T
    y3 = np.array(data[np.where(data[:,0] >= data[-1,0]-3600),1]).T
    y4 = np.array(data[np.where(data[:,0] >= data[-1,0]-3600),2]).T
    y4 = y4 * 1000
    f1, axarr = plt.subplots(2,2, sharex='col', sharey='row', figsize=(10, 6))
    axarr[0,0].plot(x1, y1)
    axarr[1,0].plot(x1, y2)
    axarr[0,1].plot(x2, y3)
    axarr[1,1].plot(x2, y4)
    axarr[1,0].set_xlabel('Time (s)')
    axarr[0,0].set_ylabel('Potential (V) vs Pt/PtO(x)')
    axarr[1,1].set_xlabel('Time (s)')
    axarr[1,0].set_ylabel('Current (mA)')
    plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
    plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
    plt.show()
    
def tunesleep(data, sleeptime, frequency, damp=0.9):
    sleeptime = sleeptime - (damp * (data[-1,0] - data[-2,0]) - sleeptime)
    return sleeptime

rm = visa.ResourceManager()
rm.list_resources()

### User defined variables:  Editable!
measurement_frequency = 1   # frequency in Hz
max_potential = 1.5
averages = 50               # set the buffer for measurements
max_current = 0.004         # Max current, in A
min_current = -max_current  # Min current, opposite of max
cutoff_hi = -0.01           # cutoff potential, in A
cutoff_lo = -1.3            # cutoff potential, in A
capacity = 5.7              # Capacity of the WE, in mA-h (depreciated, don't use)
c_rate = 1/5                # C rate
current_cap = 0             # starting capacity

### Program variables:   Edit with Caution!
sleeptime = (1/measurement_frequency)
date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
starttime = perf_counter()
data = np.reshape(([0, 0, 0, 0]), (1,4))

## Connect and Configure the instrument
sourcemeter = rm.open_resource(keithley.find2400())

keithley.initialize(sourcemeter, rsense=1)

# Loop through each current point, measure and record the voltage


sourcemeter.write(':SENSe:CURRent:PROTection ' + str(max_current))
sourcemeter.write(':SENSe:VOLTage:PROTection ' + str(max_potential))
#Source_E(sourcemeter, channel=1, E=cutoff_lo)

sourcemeter.write(':OUTP ON')
keithley.read_i(sourcemeter)
keithley.source_e(sourcemeter, 1, cutoff_lo)
sleep(1)
while keithley.read_i(sourcemeter) <= -1e-11:
 #   try:
    time = perf_counter() - starttime
    current = keithley.read_i(sourcemeter)
    potential = cutoff_lo
    current_cap = current_cap + (current * (time - data[-1,0])/3.6)
    keithley.source_e(sourcemeter, 1, potential)
    print('Time (S): {0:.2f}, Potential (V): {1:.3f}, Current (mA): {2:.3f}, Capacity (mAh): {3:.3f}'.format(time, potential, current*1000, current_cap))
    datatemp = np.reshape((time, potential, current, current_cap), (1,4))
    data = np.append(data, datatemp, axis=0)
    #sleeptime = tunesleep(data, sleeptime, measurement_frequency)
    sleep(sleeptime)
    plotdata(data)
keithley.shutdown(sourcemeter)
  #  except:
  #      keithley.initialize(sourcemeter, rsense=1)
  #      sourcemeter.write(':OUTP ON')
capacity = -np.amin(data[:,-1])
sourcemeter.write(':SENSe:CURRent:PROTection ' + str(max_current))
sourcemeter.write(':SENSe:VOLTage:PROTection ' + str(max_potential))
keithley.initialize(sourcemeter, rsense=1)
sourcemeter.write(':OUTP ON')
#capacity = -np.amin(data[:-1])
cycles = 0
while cycles <= 200:       
    while keithley.read_e(sourcemeter) >= cutoff_lo:
        time = perf_counter() - starttime
        potential = keithley.read_e(sourcemeter)
        current = - capacity * c_rate / 1000
        current_cap = current_cap + (current * (time - data[-1,0])/3.6)
        keithley.source_i(sourcemeter, 1, current)
        print('Time (S): {0:.2f}, Potential (V): {1:.3f}, Current (mA): {2:.3f}, Capacity (mAh): {3:.3f},  Cycles: {4}'.format(time, potential, current*1000, current_cap, cycles))
        datatemp = np.reshape((time, potential, current, current_cap), (1,4))
        data = np.append(data, datatemp, axis=0)
        #sleeptime = tunesleep(data, sleeptime, measurement_frequency)
        sleep(sleeptime)
        plotdata(data)
    go = time + 90
    np.savetxt('C:\Data\Charge_Discharge' + date + '.csv', data, delimiter=',', fmt='%s')
    while time <= go:
        time = perf_counter() - starttime
        potential = keithley.read_e(sourcemeter)
        current = 0
        keithley.source_i(sourcemeter, 1, current)
        print('Time (S): {0:.2f}, Potential (V): {1:.3f}, Current (mA): {2:.3f}, Capacity (mAh): {3:.3f},  Cycles: {4}'.format(time, potential, current*1000, current_cap, cycles))
        datatemp = np.reshape((time, potential, current, current_cap), (1,4))
        data = np.append(data, datatemp, axis=0)
        #sleeptime = tunesleep(data, sleeptime, measurement_frequency)
        sleep(sleeptime)
        plotdata(data)
    cycles = cycles + 1
    while keithley.read_e(sourcemeter) <= cutoff_hi:
        time = perf_counter() - starttime
        potential = keithley.read_e(sourcemeter)
        current = capacity * c_rate / 1000
        current_cap = current_cap + (current * (time - data[-1,0])/3.6)
        keithley.source_i(sourcemeter, 1, current)
        print('Time (S): {0:.2f}, Potential (V): {1:.3f}, Current (mA): {2:.3f}, Capacity (mAh): {3:.3f},  Cycles: {4}'.format(time, potential, current*1000, current_cap, cycles))
        datatemp = np.reshape((time, potential, current, current_cap), (1,4))
        data = np.append(data, datatemp, axis=0)
        #sleeptime = tunesleep(data, sleeptime, measurement_frequency)
        sleep(sleeptime)
        plotdata(data)
    go = time + 90
    np.savetxt('C:\Data\Charge_Discharge' + date + '.csv', data, delimiter=',', fmt='%s')
    while time <= go:
        time = perf_counter() - starttime
        potential = keithley.read_e(sourcemeter)
        current = 0
        current_cap = current_cap + (current * (time - data[-1,0])/3.6)
        keithley.source_i(sourcemeter, 1, current)
        print('Time (S): {0:.2f}, Potential (V): {1:.3f}, Current (mA): {2:.3f}, Capacity (mAh): {3:.3f},  Cycles: {4}'.format(time, potential, current*1000, current_cap, cycles))
        datatemp = np.reshape((time, potential, current, current_cap), (1,4))
        data = np.append(data, datatemp, axis=0)
        #sleeptime = tunesleep(data, sleeptime, measurement_frequency)
        sleep(sleeptime)
        plotdata(data)
        
keithley.shutdown(sourcemeter)
np.savetxt('C:\Data\Charge_Discharge' + date + '.csv', data, delimiter=',', fmt='%s')
