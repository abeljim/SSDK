# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 18:16:23 2019

@author: MummLab
"""

import numpy as np
import visa
import time
import bk9130
import matplotlib.pyplot as plt

#  Before running these commands, make sure that the 9130 is
#  in 'USB' mode.  To change this from the default 'GPIB':
#
#       Shift   (small blue button on the left)
#       Menu    (the I-set button, but shifted for a different function)
#       Select 'Communication' (use the arrow keys to move the blinker right)
#       Select 'USB' with the arrow keys and press 'Enter'
#       The 9130 should communicate over USB now!
#

rm = visa.ResourceManager()
instr = rm.open_resource(bk9130.find9130())

# For electrodeposition, you need to pass negative current to the cathode.
# Connect the material to be plated to the black wire and the anode 
# (source metal) to the red wire.  When a positive current is passed to
# the anode, it will dissolve, migrate to the cathode and deposit!
# Be aware of this while programming and connecting the experiment.
#
# Set the parameters here for the pulsed electrodeposition:

length = 1.5                                            # length of wire in cm
sa = (0.05*3.14*length) + 3.14*(.025*.025)              # Surface area of wire in cm^2
sc = -0.5                                               # specific current in mA / cm^2
i = -sa * sc / 1000                                     # calculate the current (in amps) for the instrument
                                                        # and flip the polarity (see the above comment) 
                      
#i = 0.00047         # Current (in Amps) to pass to the circuit.  See above!
onpulse = .1         # Time (in seconds) to apply current
offpulse = 30        # Time (in seconds) to rest
potential = 5        # overotential (in V).  Set this higher than you expect
                     # circuit to require, but keep it safe, please.
efficiency = 0.5

steps = 4000


charge = (i * onpulse * steps)
print('We are set to pass %4.3g Coulombs' % (charge))

# How many moles of electrons are passed?
mass = charge / 96485

# four electrons to reduce ionized silicon to silicon
mass = mass / 4

# convert moles to grams
mass = mass * 28.085

print('This will generate %4.3g grams of Si' % (mass * efficiency))
print('Average thickness: %4.3f μm' % (((mass / 2.320) / sa) * 10000 * efficiency))
print('Come back in %4.2f hours' % (steps * (onpulse+offpulse) / 3600))


bk9130.initialize(instr)
bk9130.source_ei(instr, E=potential, I=i)

"""
instr.write('OUTPUT ON')
#time.sleep(0.5)
if float(instr.query('MEASure:CURRent?')[:-1]) < i:
    instr.write('OUTPUT ON')
    raise Exception('Circuit can only pass ' +
                    instr.query('MEASure:CURRent?')[:-1] +
                    'A of current! Raise the "potential" variable to a higher value')
instr.write('OUTPUT OFF')
"""

n = 1
data  = []
starttime = time.perf_counter()
while n <= steps:
    print ('Step ' + str(n))
    instr.write('OUTPUT ON')
    time.sleep(onpulse)
    instr.write('OUTPUT OFF')
    time.sleep(offpulse/2)
    t = (time.perf_counter() - starttime)
    e = bk9130.read_e(instr, channel=1)
    print('Potential: %4.2g V vs counterelectrode at t = %4.2f' % (e, t))
    data.append((t, e))
    print
    time.sleep(offpulse/2)
    n = n + 1
    
data = np.asarray(data)
plt.plot(data[:,0]/3600, -data[:,1])
plt.show()
