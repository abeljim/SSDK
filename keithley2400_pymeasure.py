# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:54:17 2018

@author: MummLab
"""

import pymeasure
import time
from pymeasure.instruments.keithley import Keithley2400

sourcemeter = Keithley2400("GPIB::24::INSTR")
sourcemeter.beep(783.991,0.1)
time.sleep(0.125)
sourcemeter.beep(1046.50,0.1)
time.sleep(0.125)
sourcemeter.beep(1318.51,0.1)
time.sleep(0.125)
sourcemeter.beep(1567.98,0.22)
time.sleep(0.25)
sourcemeter.beep(1318.51,0.1)
time.sleep(0.125)
sourcemeter.beep(1567.98,0.25)
