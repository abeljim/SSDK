# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 10:09:38 2018

@author: MummLab
"""


import visa
import keithley
from time import sleep
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np


rm = visa.ResourceManager()
rm.list_resources()

sourcemeter = rm.open_resource('GPIB0::12::INSTR')
sourcemeter.write('*RST')
keithley.initialize(sourcemeter)
init = time.time()
data = [(time.time() - init, keithley.read_e(sourcemeter))]

while (time.time() - init) <= 600:
    keithley.source_i(sourcemeter, 1, I=0.001)
    data.append((time.time() - init, keithley.read_e(sourcemeter)))
    sleep(0.2)
    print('Potential (E) = ' + str(np.asarray(data)[-1,-1]) + 'V')
keithley.shutdown(sourcemeter)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(np.asarray(data)[:,0], np.asarray(data)[:,1])