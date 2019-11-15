"""
This example demonstrates how to make a graphical interface to preform
IV characteristic measurements. There are a two items that need to be 
changed for your system:
1) Correct the GPIB addresses in DepProcedure.startup for your instruments
2) Correct the directory to save files in MainWindow.queue
Run the program by changing to the directory containing this file and calling:
python iv_keithley.py
"""

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

import sys
from time import sleep
import numpy as np

from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments import Instrument
from pymeasure.log import console_log
from pymeasure.display.Qt import QtGui
from pymeasure.display.windows import ManagedWindow
from pymeasure.experiment import (
    Procedure, IntegerParameter, FloatParameter, Parameter, unique_filename, Results
)


class DepProcedure(Procedure):

    plate_e = FloatParameter('Plating Potential', units='V', minimum=-5, maximum=5, default=-1.5)
    pulse = FloatParameter('Pulse length', units='s', default=0.1)
    delay = FloatParameter('Delay Time', units='s', default=5.9)
    repeats = IntegerParameter('Cycles', units=None, default=50)
    deltat = FloatParameter('Measurement Frequency', units='Hz', default=20)
    current_range = FloatParameter('Current Range', units='A', default=0.1)
    directory = Parameter('Working Directory', default='C:/Data/')
    filename = Parameter('Filename', default=unique_filename(str(directory), prefix='Plate_'))
    DATA_COLUMNS = ['Current (A)', 'Potential (V)', 'Time (s)']

    def startup(self):
#        log.info("Setting up instruments")
#        self.meter = Keithley2182("GPIB::7::INSTR")
#        self.meter.measure_voltage()
#        self.meter.voltage_range = self.voltage_range
#        self.meter.voltage_nplc = 1 # Integration constant to Medium
        
        self.source = Keithley2400("GPIB::24::INSTR")
        self.source.apply_voltage()
        self.source.measure_current()
        self.source.voltage_nplc = 1 # Integration constant to Medium
        self.source.complinance_current = self.current_range
        self.source.enable_source()
        sleep(2)

    def execute(self):
        pulses = np.repeat(self.plate_e, (self.pulse)*1//(1/self.deltat))
        rest = np.repeat(0, (self.delay)*1//(1/self.deltat))
        potentials = np.concatenate((pulses, rest))
        potentials = np.tile(potentials, np.int(self.repeats))
#        currents *= 1e-3 # to mA from A
        steps = len(potentials)
        log.info("Starting Pulsed electrodeposition")
        for i, potential in enumerate(potentials):
            log.debug("Applying potential: %g V" % potential)

            self.source.source_voltage = potential
            # Or use self.source.ramp_to_current(current, delay=0.1)
            sleep(1/self.deltat)
            
            current = self.source.current
            time = i/self.deltat
            data = {
                'Current (A)': current,
                'Potential (V)': potential,
                'Time (s)': time
            }
            self.emit('results', data)
            self.emit('progress', 100.*i/steps)
            if self.should_stop():
                log.warning("Catch stop command in procedure")
                break

    def shutdown(self):
        self.source.shutdown()
        self.source.beep(783.991,0.1)
        sleep(0.125)
        self.source.beep(1046.50,0.1)
        sleep(0.125)
        self.source.beep(1318.51,0.1)
        sleep(0.125)
        self.source.beep(1567.98,0.22)
        sleep(0.25)
        self.source.beep(1318.51,0.1)
        sleep(0.125)
        self.source.beep(1567.98,0.25)
        log.info("Finished")


class MainWindow(ManagedWindow):

    def __init__(self):
        super(MainWindow, self).__init__(
            procedure_class=DepProcedure,
            inputs=[
                'plate_e', 'pulse', 'delay',
                'repeats', 'deltat', 'current_range', 'filename'
            ],
            displays=[
                'plate_e', 'pulse', 'delay',
                'repeats', 'deltat', 'current_range'
            ],
            x_axis='Time (s)',
            y_axis='Potential (V)'
        )
        self.setWindowTitle('Pulsed Electrodeposition - E')

    def queue(self):
        filename = str(DepProcedure.filename)
#        filename = unique_filename(directory, prefix='IV')

        procedure = self.make_procedure()
        results = Results(procedure, filename)
        experiment = self.new_experiment(results)

        self.manager.queue(experiment)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
sys.exit(app.exec_())