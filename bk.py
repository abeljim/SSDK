# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:19:39 2018

@author: MummLab
"""

from time import sleep
import visa
import numpy as np
rm = visa.ResourceManager()

def initialize(instr):
    instr.write('*RST')
    sleep(0.5)   # wait here to give the instrument time to react


def source(instr, channel, e, i):
    instr.write('APPL CH' + str(channel) + ',' + str(e) + ',' + str(i))

def enable(instr, channels):
    query = instr.query('APPLY:OUTput?')
    query.rstrip('\n')
    query.rstrip(' ')
    query = query.split(',')
    enabled = np.array([int(i) for i in query])
    enabled = np.concatenate((np.ones(1), enabled))
    enabled[channels] = 1
    instr.write('APPLY:OUT ' + str(int(enabled[1])) + ',' + str(int(enabled[2])) + ',' + str(int(enabled[3])))
    
def disable(instr, channels):
    query = instr.query('APPLY:OUTput?')
    query.rstrip('\n')
    query.rstrip(' ')
    query = query.split(',')
    enabled = np.array([int(i) for i in query])
    enabled = np.concatenate((np.ones(1), enabled))
    enabled[channels] = 0
    instr.write('APPLY:OUT ' + str(int(enabled[1])) + ',' + str(int(enabled[2])) + ',' + str(int(enabled[3])))
        
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

def shutdown(instr):
    instr.write('APPLY:OUT 0,0,0')
    instr.write('SYSTem:BEEPer,0.1')
    sleep(0.25)
    instr.write('SYSTem:BEEPer,0.1')
    sleep(0.125)
    instr.write('SYSTem:BEEPer,0.1')
    sleep(0.125)
    instr.write('SYSTem:BEEPer,0.22')
    sleep(0.25)
    instr.write('SYSTem:BEEPer,0.1')
    sleep(0.5)
    instr.write('SYSTem:BEEPer,0.25')
    sleep(0.25)
    instr.write('SYSTem:BEEPer,0.1')
    instr.write('*RST')
    
def reset(instr):
    print("Exception Raised!  Attempting to reset...")
    sleep(0.5)
    instr.close()
    sleep(0.5)
    instr = rm.open_resource([i for i in rm.list_resources() if '9130' in i][0])
    sleep(0.5)
    initialize(instr)
    sleep(0.5)