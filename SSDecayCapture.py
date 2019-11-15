"""
Created on Tue Nov  5 20:10:05 2019
@author: SierraGross

For capturing steady state and decay of bubbles from electrode surface
Uses Kiethley 2400

Experimental Setup: 5 min to SS, 101 images at SS, and 20 min decay

"""

import visa
import keithley
import time
import numpy as np

rm = visa.ResourceManager()
rm.list_resources()
sourcemeter = rm.open_resource('GPIB0::12::INSTR')
keithley.initialize(sourcemeter)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        print('\n')
        time.sleep(1)
        t -= 1
def signal():
    sourcemeter.write('SYSTem:BEEPer 523.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 659.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 783.99,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 1046.50,0.1')

# times and frames for each step 
tss = 5*60  # SS time in seconds
fss = tss*(10/17.95) # frames of SS condition
td = 20*60  # decay time in seconds
fd = td/5   # frames of decay condition 


# Currents to be tested
i = [0.00005, 0.000100,0.000250]

# image capture loop
for j in range(3): # number of replicates
    for k in range((len(i)-1)): # counts currents
        # Prime the Electrode
        keithley.source_i(sourcemeter, I=0.001)
        sourcemeter.write(':OUTP ON')
        countdown(60)
        signal()
        #if checking for bubble build up
        #wait = input("Press enter if bubbles are built up")
        sourcemeter.write('OUTP OFF')
        countdown(120)
        
        # Reaching SS
        print("reaching SS")
        keithley.source_i(sourcemeter,I = i[j]) # set current
        sourcemeter.write('OUTP ON') # run current
        countdown(300)
        signal() # signals SS is reached
        
        # Capture SS Images
        print("change folder name")
        wait = input("SS is reached, press enter to take pictures")
        countdown(tss)
        signal() # signals SS images are captured
        
        ## Capture Decay Images
        print("change folder name")
        wait = input("SS images captured, press enter for decay (no delay)")
        #wait = input("SS images captured, press enter for decay (5s delay)")
        #countdown(5) # 5 second countdown before starting image capture
        sourcemeter.write('OUTP OFF')
        countdown(td)
        signal()
        
# image capture individual (repeat 3 times)
# Prime the Electrode
keithley.source_i(sourcemeter, I=0.001)
sourcemeter.write(':OUTP ON')
countdown(60)
signal()
#if checking for bubble build up
wait = input("Press enter if bubbles are built up")
sourcemeter.write('OUTP OFF')
countdown(120)

#i = 0.00005
i = 0.000100
#i = 0.000250

# Reaching SS
print("reaching SS")
keithley.source_i(sourcemeter,I = i) # set current
sourcemeter.write('OUTP ON') # run current
countdown(300)
signal() # signals SS is reached



## Capture Decay Images
print("change folder name")
wait = input("SS images captured, press enter for decay (no delay)")
#wait = input("SS images captured, press enter for decay (5s delay)")
#countdown(5) # 5 second countdown before starting image capture
sourcemeter.write('OUTP OFF')
countdown(td)
signal()