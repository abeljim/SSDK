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
    capacity = FloatParameter('Capacity', units='mAh', minimum=0, maximum = 10, default=4.29)
    c_rate = FloatParameter('Charge Rate', units='C', minimum=0.01, maximum = 20, default=1)
    repeats = IntegerParameter('Cycles', units=None, minimum=1, maximum=1e8, default=50)
    deltat = FloatParameter('Measurement Frequency', units='Hz', default=1)
    voltage_range = FloatParameter('Potential Range', units='V', default=10)
    directory = Parameter('Working Directory', default='C:/Data/')
    filename = Parameter('Filename', default=unique_filename(str(directory), prefix='charge_'))
    DATA_COLUMNS = ['Time (s)', 'Current (A)', 'Potential (V)']

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
        self.source.source_current()
        self.source.measure_voltage()
        self.source.source_current_range = self.capacity*self.c_rate*5
        self.source.compliance_voltage = self.voltage_range
        self.source.enable_source()
        sleep(2)

    def execute(self):
        charge_rate = self.capacity*self.c_rate*0.001   # Charge rate, in A
        discharge_rate = charge_rate*-1     # Discharge rate, in A
        currents = np.repeat(charge_rate, )
        currents_up = np.arange(self.min_current, self.max_current, self.current_step)
        currents_down = np.arange(self.max_current, self.min_current, -self.current_step)
        
        currents = np.concatenate((currents_up, currents_down)) # Include the reverse
        currents *= 1e-3 # to mA from A
        steps = len(currents)
        
        # To calculate the e_step, convert to V/s and divide by measurement frequency 
        self.source.ramp_to_voltage(hi_e)
        e_step = 0.001*self.sweep_rate/self.deltat
        sweep1 = np.arange(in_e, hi_e, e_step)
        sweep2 = np.arange(hi_e, lo_e, -e_step)
        sweep3 = np.arange(lo_e, hi_e, e_step)
        potentials = np.concatenate((sweep2, sweep3))
        potentials = np.tile(potentials, np.int(self.repeats))
        sweep4 = np.arange(hi_e, in_e, -e_step)
        potentials = np.concatenate((sweep1, potentials))
        potentials = np.concatenate((potentials, sweep4))
        steps = len(potentials)
        log.info("Starting Discharge-Charge")

        for i, e in enumerate(potentials):
            log.debug("Measuring potential: %g V" % e)
            self.source.source_voltage = e
            sleep(1/self.deltat)
            current = self.source.current
            time = i/self.deltat
            data = {
                    'Time (s)': time,
                    'Potential (V)': e,
                    'Current (A)': current
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
                'in_e', 'lo_e', 'hi_e', 'sweep_rate',
                'repeats', 'deltat', 'voltage_range', 'current_range', 'filename'
            ],
            displays=[
                'in_e', 'lo_e', 'hi_e', 'sweep_rate',
                'repeats', 'deltat', 'voltage_range', 'current_range'
            ],
            x_axis='Potential (V)',
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