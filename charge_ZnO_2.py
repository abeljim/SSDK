# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:35:47 2018

@author: MummLab
"""

from time import perf_counter
from time import sleep
import numpy as np
import datetime
import visa
import keithley
import matplotlib
import matplotlib.pyplot as plt

def plotdata(data):
    x = np.array(data[:,0], dtype=float)
    y = np.array(data[:,2], dtype=float)
    plt.plot(x, y)
    plt.ylabel('Current (A)')
    plt.xlabel('Time (s)')
    plt.show()
    
rm = visa.ResourceManager()
rm.list_resources()
sourcemeter = rm.open_resource('GPIB0::12::INSTR')
#cap = cv2.VideoCapture(0)

### User defined variables:  Editable!
measurement_frequency = 1   # frequency in Hz
max_current = 0.15           # Max current, in A
min_current = -max_current  # Min current, opposite of max
cutoff = -55                # cutoff current, in microamps
potential = -1.6           # potential at which to hold WE

date = datetime.datetime.now()
date = date.strftime('%Y-%m-%d_%H-%M-%S')
starttime = perf_counter()
data = np.reshape(('Time', 'Potential (V)', 'Current (A)'), (1,3))

keithley.initialize(sourcemeter, rsense=1)
keithley.source_e(sourcemeter, E=potential)
sourcemeter.write(':SENSe:CURRent:PROTection ', str(max_current))
sourcemeter.write(':OUTP ON')
current = keithley.read_i(sourcemeter)
while current <= cutoff/1000000:
    try:
        time = perf_counter()
        time = time - starttime
#        sourcemeter.measure_voltage()
        potential2 = potential
#        potential = sourcemeter.voltage
#        sourcemeter.measure_current()
        current = keithley.read_i(sourcemeter)
#        ret, frame = cap.read()
        print('Time (S): {0:.2f}, Potential (V): {1:.3f}, Current (mA): {2:.3f}'.format(time, potential2, current*1000))
        datatemp = np.reshape((time, potential, current), (1,3))
        data = np.append(data, datatemp, axis=0)
#        cv2.imwrite('C:\Data\'' + str(date) + '\charge_' + str(time) + '.png', frame)
        plotdata(data[1:])
        sleep(1/measurement_frequency)
#        cap.release()
    except VisaIOError: 
        print("Exception Raised!  Attempting to reset...")

        sourcemeter.close()
        sourcemeter = rm.open_resource('GPIB0::5::INSTR')
        sleep(1)
        keithley.initialize(sourcemeter)
        keithley.source_e(sourcemeter, E=potential)
        sourcemeter.write(':SENSe:CURRent:PROTection ', str(max_current))
        sourcemeter.write(':OUTP ON')
        
        
keithley.shutdown(sourcemeter)
fig, ax = matplotlib.pyplot.subplots()
ax.plot(np.asarray(data[1:], dtype=float)[:,0],
        1000*np.asarray(data[1:], dtype=float)[:,2])
ax.set(xlabel='Time (s)', ylabel='Current (mA)')
ax.grid()
matplotlib.pyplot.show()

np.savetxt('C:\Data\Charge_powder' + date + '.csv', data, delimiter=',', fmt='%s')
plt.plot(data[:,0], data[:,1])
plt.plot(data[:,0], data[:,2])
