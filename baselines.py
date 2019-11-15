# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:28:02 2019

@author: MummLab
"""


import visa
import keithley
#import bk9130
import time
import numpy as np


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        print('\n')
        time.sleep(1)
        t -= 1

rm = visa.ResourceManager()
rm.list_resources()

#light = rm.open_resource('GPIB0::15::INSTR')
sourcemeter = rm.open_resource('GPIB0::12::INSTR')

keithley.initialize(sourcemeter)

#keithley.source_i(sourcemeter, I=0.00005)
sourcemeter.write(':OUTP ON')
# build up the baseline images

#time.sleep(300)
#forward
for i in [0.000025, 0.000050, 0.000100, 0.000150, 0.000200, 0.000250,
          0.000300, 0.000350, 0.000400, 0.000450, 0.000500]:
    print(i)
for i in [0.000250, 0.000300, 0.000350, 0.000400, 0.000450, 0.000500]:
#reverse
#for i in [0.000500, 0.000450, 0.000400, 0.000350, 0.000300, 0.000250,
#          0.000200, 0.000150, 0.000100, 0.000050, 0.000025]:    
    # Take pictures of the static conditions:
    keithley.source_i(sourcemeter, I=i)
    sourcemeter.write('OUTP ON')
    countdown(60)
    sourcemeter.write('SYSTem:BEEPer 523.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 659.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 783.99,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 1046.50,0.1')
    # Take static pictures here:
    wait = input("TAKE STATIC PICTURES HERE (PRESS ENTER WHEN YOU START).")
    countdown(510)
    sourcemeter.write('SYSTem:BEEPer 523.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 659.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 783.99,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 1046.50,0.1')
    wait = input("PRESS ENTER TO START THE NEXT CURRENT.")

    
    
for i in [0.0000100, -0.000025, -0.000500]:
    keithley.source_i(sourcemeter, I=-i)
    sourcemeter.write('OUTP ON')    
    countdown(1200)
    sourcemeter.write('SYSTem:BEEPer 523.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 659.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 783.99,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 1046.50,0.1')
    """
    Take pictures here
    """
    wait = input("PRESS ENTER TO CONTINUE.")
    sourcemeter.write('OUTP OFF')    
    countdown(1200))
    sourcemeter.write('SYSTem:BEEPer 523.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 659.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 783.99,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 1046.50,0.1')
    
#    light.write('OUTP OFF')

sourcemeter.write('OUTP OFF')
keithley.initialize(sourcemeter)

time.sleep(600)
keithley.source_i(sourcemeter, I=0.000500)