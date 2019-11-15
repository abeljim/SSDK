# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 13:35:39 2018

@author: Kyle McDevitt (kmmcdev@gmail.com)
"""
"""
A collection of functions for the Keithley 2400 Sourcemeter
"""
import numpy as np
import visa
import sys
rm = visa.ResourceManager()

"""
This function will measure either the potential across or the current through the
instrument.  It accepts three arguments (instrument, measurement, and repeats),
though if only the instrument is specified, the default is to meausure potential
and to only do it once.  The third variable will define how many repeats to average
"""
def find_sourcemeter():

    name = 'dummy'
    n = 0
    while name[:36] != 'KEITHLEY INSTRUMENTS INC.,MODEL 2400':
        instruments = rm.list_resources()
        try:
            sourcemeter = rm.open_resource(instruments[n])
        except IndexError:
            print ('Sourcemeter not Found!')
            sys.exit()
        try:
            name = sourcemeter.query('*IDN?')
        except:
            n = n+1
    return instruments[n]

def measure(instr, m='E', time=1):
    instr.write('*RST')
    if m == 'E':
        instr.write(':SOUR:FUNC CURR')
        instr.write(':SOUR:CURR:MODE FIXED')
        instr.write(':SENS:FUNC "VOLT"')
        instr.write(':SOUR:CURR:RANG MIN')
        instr.write(':SOUR:CURR:LEV 0')
        instr.write(':SENS:VOLT:PROT 25')
        instr.write(':SENS:VOLT:RANG 20')
        instr.write(':FORM:ELEM VOLT')
    if m == 'I':
        instr.write(':SOUR:FUNC VOLT')
        instr.write(':SOUR:VOLT:MODE FIXED')
        instr.write(':SENS:FUNC "CURR"')
        instr.write(':SOUR:VOLT:RANG MIN')
        instr.write(':SOUR:VOLT:LEV 0')
        instr.write(':SENS:CURR:PROT 1')
        instr.write(':SENS:CURR:RANG AUTO')
        instr.write(':FORM:ELEM CURR')   
    instr.write(':OUTP ON')
    out=[]
    n = 0
    while n < time:
        out.append(float(instr.query(':READ?').rstrip()))
        n = n + 1
    instr.write(':OUTP OFF')
    return np.nanmean(out)

"""
def source(instr, m='E', time=1):
    instr.write('*RST')
    if m == 'E':
        instr.write(':SOUR:FUNC VOLT')
        instr.write(':SOUR:VOLT:MODE FIXED')
        instr.write(':SENS:FUNC "CURR"')
        instr.write(':SOUR:VOLT:RANG MIN')
        instr.write(':SOUR:VOLT:LEV 0')
        instr.write(':SENS:CURR:PROT 1')
        instr.write(':SENS:CURR:RANG AUTO')
        instr.write(':FORM:ELEM CURR')
        
        return i 
"""
find_sourcemeter()
def printscreen(instr, screen, string):
    