# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 17:01:41 2018

@author: MummLab
"""

import visa
import keithley
from time import sleep

rm = visa.ResourceManager()
rm.list_resources()

sourcemeter = rm.open_resource('GPIB0::12::INSTR')
sourcemeter.write('*RST')
keithley.initialize(sourcemeter)
#A = 0.0104       # surface area in cm^2
#A = 2.56 * 0.047 # (planar samples)
#A = 0.585        # (Hot Pressed sample (polished))
#A = 0.14        # (PED)
#A = 0.38 # B20 medium
#A = 0.153 # B18 sm
A=0.159 #Ni wires
c = -A/100 # current in amps
livetime = 20 # time current is on (s)
cycles = 9 # number of cycles - 1

# normalize
sleep(5)
keithley.source_i(sourcemeter, I= 4*c)
sourcemeter.write(':OUTP ON')
sleep(20)
sourcemeter.write(':OUTP OFF')
sleep(10)
sourcemeter.write(':OUTP ON')
sleep(15)
sourcemeter.write(':OUTP OFF')
sleep(10)
keithley.shutdown(sourcemeter)



# J = 5 mA/cm^2
keithley.source_i(sourcemeter, I= c *0.5)
n = 0
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)

# J = 10 mA/cm^2
keithley.source_i(sourcemeter, I= c)
n = 0
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)

# J = 15 mA/cm^2
keithley.source_i(sourcemeter, I= c *1.5)
n = 0
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)

# J = 20 mA/cm^2    
keithley.source_i(sourcemeter, I= c * 2)
n = 0
sourcemeter.write(':OUTP OFF')
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)

# J = 25 mA/cm^2
keithley.source_i(sourcemeter, I= c *2.5)
n = 0
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)

# J = 30 mA/cm^2
keithley.source_i(sourcemeter, I= c * 3)
n = 0
sourcemeter.write(':OUTP OFF')
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)

# J = 35 mA/cm^2
keithley.source_i(sourcemeter, I= c *3.5)
n = 0
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)

# J = 40 mA/cm^2
keithley.source_i(sourcemeter, I= c *4)
n = 0
sleep(10)
while n <= cycles:
    sourcemeter.write(':OUTP ON')
    sleep(livetime)
    sourcemeter.write(':OUTP OFF')
    sleep(25)
    n = n+1
sleep(20)
sleep(20)
keithley.shutdown(sourcemeter)
