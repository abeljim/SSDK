import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

import sys
from time import sleep
import numpy as np

from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments import Instrument

capacity = 10.69    # measured capacity in Coulombs
capacity = 10.69 - 1.04 # loss due to background current
capacity = capacity * 0.2777778 # Convert capacity to mAh
rate = 10
rest = 600
current = capacity * 0.001 / rate

source = Keithley2400("GPIB::24::INSTR")
source.apply_current()
source.measure_voltage()
source.source_current_range = current * 2 # Current range is 2x
source.compliance_voltage = 3
source.enable_source()

initial_e = source.voltage

i = 0
while i < 7:
  source.source_current = current
  sleep(1800)
  source.source_current = 0
  sleep(110)
  print("E = ", source.voltage)
  sleep(10)
  sleep(634)
  sleep(120)
  i = i + 1
  