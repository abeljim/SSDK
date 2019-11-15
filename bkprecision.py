# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a library I am using to define functions for the Ketihley instruments
"""
from time import sleep
import visa
import numpy as np
rm = visa.ResourceManager()

def initialize(instr):
    instr.write('*RST')
    sleep(0.5)   # wait here to give the instrument time to react

def source_e(instr, channel=1, E=1):
    instr.write(':SOURce:CURRent:MODE SWEep')
    instr.write(':SOURce:VOLTage:MODE FIX')
    instr.write(':SOURce:VOLTage:RANGE:AUTO 1')
    instr.write(':SOURce:VOLTage:LEVel ', str(E))
    
def beep():
    instr.write(':SYSTem:BEEPer')
    
"""

def source_i(instr, channel=1, I=0):
    instr.write(':SOURce:FUNCtion:MODE CURR')
    instr.write(':SOURce:CURRent:MODE FIX')
    instr.write(':SOURce:CURRent:RANGE:AUTO 1')
    instr.write(':SOURce:CURRent:LEVel ', str(I))
    
def read_e(instr, channel=1):
    instr.write(':CONFigure:Voltage')
    instr.write(':FORMat:ELEMents VOLT')
    instr.write(':SENSe:FUNCtion:OFF "CURRent"')
    instr.write(':SENSe:FUNCtion:ON "VOLTage"')
    instr.write(':SENSe:FUNCtion:OFF "Resistance"')
    e = float(instr.query(':READ?'))
    return e
    
def read_i(instr, channel=1, E=1):
    instr.write(':CONFigure:Current')
    instr.write(':FORMat:ELEMents CURR')
    instr.write(':SENSe:FUNCtion:ON "CURRent"')
    instr.write(':SENSe:FUNCtion:OFF "VOLTage"')
    instr.write(':SENSe:FUNCtion:OFF "Resistance"')
    i = float(instr.query(':READ?'))
    return i

def sweep_i(instr, i0, i1, time, points=100, channel=1, log=False):
    instr.write(':SOURce:FUNCtion:MODE CURR')
    instr.write(':SOURce:CURRent:MODE FIX')
    instr.write(':SOURce:CURRent:RANGE:AUTO 1')
    if log == True:
        endtime = np.log10(time)
        times = np.logspace(0, endtime, points)
    else:
        times = np.linspace(0, time, points)
    steps = np.zeros((points, 2))
    steps[:,0] = np.gradient(times)
    steps[:,1] = np.linspace(i0, i1, points) 
    instr.write(':OUTP ON')
    instr.write(':SOURce:CURRent:LEVel ', str(i0))
    for step in steps:
        sleep(step[0])
        instr.write(':SOURce:CURRent:LEVel ', str(step[1]))

def sweep_e(instr, e0, e1, time, points=100, channel=1, log=False):
    instr.write(':SOURce:CURRent:MODE SWEep')
    instr.write(':SOURce:VOLTage:MODE FIX')
    instr.write(':SOURce:VOLTage:RANGE:AUTO 1')
    if log == True:
        endtime = np.log10(time)
        times = np.logspace(0, endtime, points)
    else:
        times = np.linspace(0, time, points)
    steps = np.zeros((points, 2))
    steps[:,0] = np.gradient(times)
    steps[:,1] = np.linspace(e0, e1, points)
    instr.write(':SOURce:VOLTage:LEVel ', str(e0))
    instr.write(':OUTP ON')
    for step in steps:
        sleep(step[0])
        instr.write(':SOURce:VOLTage:LEVel ', str(step[1]))
        
def shutdown(instr):
    instr.write('SYSTem:BEEPer 783.991,0.1')
    sleep(0.125)
    instr.write('SYSTem:BEEPer 1046.50,0.1')
    sleep(0.125)
    instr.write('SYSTem:BEEPer 1318.51,0.1')
    sleep(0.125)
    instr.write('SYSTem:BEEPer 1567.98,0.22')
    sleep(0.25)
    instr.write('SYSTem:BEEPer 1318.51,0.1')
    sleep(0.125)
    instr.write('SYSTem:BEEPer 1567.98,0.25')
    instr.write('*RST')
    
def reset(instr, max_current=0.03, max_potential=1.5):
    print("Exception Raised!  Attempting to reset...")
    sleep(0.5)
    instr.close()
    sleep(0.5)
    instr = rm.open_resource('GPIB0::5::INSTR')
    sleep(0.5)
    initialize(instr)
    instr.write(':SENSe:CURRent:PROTection ' + str(max_current))
    instr.write(':SENSe:VOLTage:PROTection ' + str(max_potential))
    sleep(0.5)
"""