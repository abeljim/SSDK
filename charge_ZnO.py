# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:35:47 2018

@author: MummLab
"""

from time import perf_counter
from time import sleep
import numpy as np
from pymeasure.instruments.keithley import Keithley2400
import datetime

def shutdown(unit):
    unit.shutdown()
    unit.beep(783.991,0.1)
    sleep(0.125)
    unit.beep(1046.50,0.1)
    sleep(0.125)
    unit.beep(1318.51,0.1)
    sleep(0.125)
    unit.beep(1567.98,0.22)
    sleep(0.25)
    unit.beep(1318.51,0.1)
    sleep(0.125)
    unit.beep(1567.98,0.25)

def initialize(unit):
    unit = Keithley2400("GPIB::24::INSTR")
    unit.reset()
    unit.use_front_terminals()
    unit.measure_current()
    unit.write("SYST:RSEN ON")
    sleep(3)   # wait here to give the instrument time to react
    

### User defined variables:  Editable!
measurement_frequency = 1   # frequency in Hz
max_current = 0.1           # Max current, in A
min_current = -max_current  # Min current, opposite of max
cutoff = -0.005             # cutoff current, in A
potential = -1.55           # potential at which to hold WE


### Experimental variables:  Edit with caution
date = datetime.datetime.now()
date = date.strftime('%Y-%m-%d_%H-%M-%S')
starttime = perf_counter()
data = np.reshape(('Time', 'Potential (V)', 'Current (A)'), (1,3))

# Connect and Configure the instrument
sourcemeter = Keithley2400("GPIB::24::INSTR")
initialize(sourcemeter)

sourcemeter.enable_source()
sourcemeter.source_voltage = potential
sourcemeter.compliance_current = max_current

# Loop through each current point, measure and record the voltage
while sourcemeter.current <= cutoff:
    try:
        time = perf_counter()
        time = time - starttime
#        sourcemeter.measure_voltage()
        potential2 = potential
#        potential = sourcemeter.voltage
#        sourcemeter.measure_current()
        current = sourcemeter.current
        print('Time (S): {0:.2f}, Potential (V): {1:.3f}, Current (mA): {2:.3f}'.format(time, potential2, current*1000))
        datatemp = np.reshape((time, potential, current), (1,3))
        data = np.append(data, datatemp, axis=0)
        sleep(1/measurement_frequency)
    except: 
        print("Exception Raised!  Attempting to reset...")
        sleep(3)
        sourcemeter = Keithley2400("GPIB::24::INSTR")
        initialize(sourcemeter)
          
shutdown(sourcemeter)
np.savetxt('C:\Data\Charge_' + date + '.csv', data, delimiter=',', fmt='%s')
