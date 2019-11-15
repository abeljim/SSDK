# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:46:34 2018

@author: MummLab
"""

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

import sys
from time import sleep
import numpy as np

from pymeasure.instruments.keithley import Keithley2400
#from pymeasure.instruments import Instrument
#from pymeasure.log import console_log
from pymeasure.display.Qt import QtGui
from pymeasure.display.windows import ManagedWindow
from pymeasure.experiment import (
    Procedure, IntegerParameter, FloatParameter, Parameter, unique_filename, Results
    )

in_e = 0
lo_e = -50
hi_e = 50
sweep_rate = 10
repeats = 5
deltat = 5
current_step = sweep_rate/deltat


in_e = in_e/1000
lo_e = lo_e/1000
hi_e = hi_e/1000
e_step = 0.001*sweep_rate/deltat
sweep1 = np.arange(in_e, hi_e, e_step)
sweep2 = np.arange(hi_e, lo_e, -e_step)
sweep3 = np.arange(lo_e, hi_e, e_step)
potentials = np.concatenate((sweep2, sweep3))
potentials = np.tile(potentials, np.int(repeats))
sweep4 = np.arange(hi_e, in_e, -e_step)
potentials = np.concatenate((sweep1, potentials))
potentials = np.concatenate((potentials, sweep4))

source = Keithley2400("GPIB::24::INSTR")
source.apply_voltage()
source.measure_current()
source.enable_source()

for e in potentials:
#    log.debug("Measuring potential: %g V" % e)
    source.source_voltage = e
    sleep(1/deltat)
    current = source.current
    data = {
            'Potential (V)': e,
            'Current (A)': current
            }
            
        """
        pulses = np.repeat(self.plate_current, (self.pulse)*1//(1/self.deltat))
        rest = np.repeat(0, (self.delay)*1//(1/self.deltat))
        potentials = np.concatenate((pulses, rest))
        potentials = np.tile(potentials, np.int(self.repeats))
        steps = len(potentials)
        
        """
source.ramp_to_voltage(hi_e, steps=30, pause=0.02)
