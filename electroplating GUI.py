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
#from pymeasure.instruments import Instrument
#from pymeasure.log import console_log
from pymeasure.display.Qt import QtGui
from pymeasure.display.windows import ManagedWindow
from pymeasure.experiment import (
    Procedure, IntegerParameter, FloatParameter, Parameter, unique_filename, Results
)

class DepProcedure(Procedure):

    plate_current = FloatParameter('Plating Current', units='A', minimum=-1, maximum=1, default=0.000268055577)
    pulse = FloatParameter('Pulse length', units='s', maximum=1e8, default=0.1)
    delay = FloatParameter('Delay Time', units='s', maximum=1e8, default=5.9)
    repeats = IntegerParameter('Cycles', units=None, minimum=1, maximum=1e8, default=500)
    deltat = FloatParameter('Measurement Frequency', units='Hz', default=20)
    voltage_range = FloatParameter('Potential Range', units='V', default=10)
    directory = Parameter('Working Directory', default='C:/Data/')
    filename = Parameter('Filename', default=unique_filename(str(directory), prefix='Plate_'))
    DATA_COLUMNS = ['Current (A)', 'Potential (V)', 'Time (s)']

    def startup(self):
        log.info("Setting up instruments")
        """
        To use the Nanovoltmeter instead of the Sourcemeter to measure
        potential, uncomment the following section and change the corresponding
        section in execute routine to measure from meter instead of source    
        """
#        self.meter = Keithley2182("GPIB::7::INSTR")
#        self.meter.measure_voltage()
#        self.meter.voltage_range = self.voltage_range
#        self.meter.voltage_nplc = 1 # Integration constant to Medium
        
        self.source = Keithley2400("GPIB::24::INSTR")
        self.source.apply_current()
        self.source.measure_voltage()
        self.source.source_current_range = self.plate_current*1.1 # Current range is 10% over target
        self.source.compliance_voltage = self.voltage_range
        self.source.enable_source()
        sleep(2)

    def execute(self):
        pulses = np.repeat(self.plate_current, (self.pulse)*1//(1/self.deltat))
        rest = np.repeat(0, (self.delay)*1//(1/self.deltat))
        currents = np.concatenate((pulses, rest))
        currents = np.tile(currents, np.int(self.repeats))
#        currents *= 1e-3 # to mA from A
        steps = len(currents)
        log.info("Starting Pulsed electrodeposition")
        for i, current in enumerate(currents):
            log.debug("Applying current: %g A" % current)

            self.source.source_current = current
            # Or use self.source.ramp_to_current(current, delay=0.1)
            sleep(1/self.deltat)
            
            voltage = self.source.voltage
            time = i/self.deltat
            data = {
                'Current (A)': current,
                'Potential (V)': voltage,
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
                'plate_current', 'pulse', 'delay',
                'repeats', 'deltat', 'voltage_range', 'filename'
            ],
            displays=[
                'plate_current', 'pulse', 'delay',
                'repeats', 'deltat', 'voltage_range'
            ],
            x_axis='Time (s)',
            y_axis='Current (A)'
        )
        self.setWindowTitle('Pulsed Electrodeposition - I')

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