# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:48:15 2018

@author: MummLab
"""

import numpy as np
import visa
rm = visa.ResourceManager()
rm.list_resources()
nanovoltmeter = rm.open_resource('GPIB0::11::INSTR')
nanovoltmeter.query('*IDN?')
nanovoltmeter.write('*RST')
#
#sourcemeter = rm.open_resource('GPIB0::12::INSTR')
#sourcemeter.query('*IDN?')
#sourcemeter.write('*RST')

solartron1 = rm.open_resource('GPIB0::2::INSTR')
solartron11 = rm.open_resource('GPIB0::3::INSTR')
#solartron1.query('*IDN?')
solartron1.write('PO0') # Operate as potentiostat
solartron1.write('BK4') # reset

solartron2 = rm.open_resource('GPIB0::4::INSTR', send_end=False)
solartron22 = rm.open_resource('GPIB0::5::INSTR')
solartron2.query('*IDN?')
solartron2.write('*RST')


def solartron_cv(instrument, v1, v2, speed, repeat):
    from time import sleep
    import numpy as np
    instrument.write('BK4')
    sleep(1)
    # Time for each sweep step
    time = np.absolute(1000 * (v2 - v1) / speed)
    
    # v1 = va = vb
    # v2 = vc = vd
    # ta = 0
    # tb = time
    # tc = 0
    # td = time
    
    
    # Set the end condition (standby)
    instrument.write('OF0')
    
    # Set sweep segment
    instrument.write('SM'+str(repeat*4))
    
    instrument.write('VA'+str(v1))
    instrument.write('TA'+str(0.01))
    instrument.write('VB'+str(v1))
    instrument.write('TB'+str(time))
    
    instrument.write('VC'+str(v2))
    instrument.write('TC'+str(0.01))
    instrument.write('VD'+str(v2))
    instrument.write('TD'+str(time))
    
    # Set DVM to 5x9
    instrument.write('DG0')
    # Set X to be the potential of RE1 vs RE2
    instrument.write('PX3')
    # Set Y to be current
    instrument.write('PY5')
    # Set DVM to continuous measurements
    # TR0 = single TR1 = continuous TR2 = External (trigger) TR3 = Sync
    instrument.write('TR3')
    # Set overload condition:  OL0 = cutout OL1 = limit OL2 = No limit
    instrument.write('OL2')
    instrument.write('SV255')    
    
    print('Starting sweep in 5 seconds')
    sleep(1)
    print('Starting sweep in 4 seconds')
    sleep(1)
    print('Starting sweep in 3 seconds')
    sleep(1)
    print('Starting sweep in 2 seconds')
    sleep(1)
    print('Starting sweep in 1 seconds')
    sleep(1)
    print('Starting sweep!')

    # Turn on cell polarization
    instrument.write('PW1')
    # start the DVM
    instrument.write('RU1')
    # Start the sweep
    instrument.write('SW1')
    print('Experiment will take '+str(time*2*repeat)+' seconds')

    # Set GPIB data output to Long Dump (binary) 
    instrument.write('GP1')
    # Set output separator to comma
    instrument.write('OS0')    
    
    sleep(time*2*repeat)
    # Stop the DVM    
    instrument.write('RU0')
    # Stop the sweep
    instrument.write('SW0')
    #turn off cell polarization
    instrument.write('PW0')
    return
