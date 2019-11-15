"""
This example demonstrates how to make a graphical interface to preform
IV characteristic measurements. There are a two items that need to be 
changed for your system:
1) Correct the GPIB addresses in IVProcedure.startup for your instruments
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
    Procedure, FloatParameter, Parameter, unique_filename, Results
)


class PotentiostaticProcedure(Procedure):

    potential = FloatParameter('Potential', units='V', default=0.1)
    max_current = FloatParameter('Maximum Current', units='mA', default=10)
    time = FloatParameter('Experiment Length', units='s', default=5)
    dt = FloatParameter('Measurement frequency', units='Hz', default=5)
    voltage_range = FloatParameter('Voltage Range', units='V', default=10)
    directory = Parameter('Working Directory', default='C:/Data/')
    filename = Parameter('Filename', default=unique_filename(str(directory), prefix='StaticE'))
    DATA_COLUMNS = ['Time (s)', 'Current (A)', 'Potential (V)']

    def startup(self):
        
        self.source = Keithley2400("GPIB::24::INSTR")
        self.source.apply_voltage(voltage_range=None,
                                  compliance_current=0.1)
        self.source.measure_current(nplc=1, 
                                    current=self.max_current,
                                    auto_range=True)
#        self.source.apply_current()
#        self.source.source_current_range = self.max_current*1e-3 # A
#        self.source.complinance_voltage = self.voltage_range
        self.source.enable_source()
        sleep(2)

    def execute(self):
        potential = self.potential
        times = np.arange(0,
                            self.time,
                            1/self.dt)
        steps = len(times)
        log.info("Applying potential of %f V" % potential)
        self.source.source_voltage = potential
        for i, time in enumerate(times):
#            self.source.source_current = potential
            sleep(1/self.dt) 
            # sleep between current measurements (Hz -> s)
            
            current = self.source.current

            data = {
#                'Time (s)': time,
                'Potential (V)': potential,
                'Current': current
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
            procedure_class=PotentiostaticProcedure,
            inputs=[
                'potential', 'max_current', 'time',
                'dt', 'voltage_range', 'filename'
            ],
            displays=[
                'potential', 'max_current', 'time',
                'dt', 'voltage_range'
            ],
            x_axis='Time (s)',
            y_axis='Current (A)'
        )
        self.setWindowTitle('Potentiostatic')

    def queue(self):
        filename = str(PotentiostaticProcedure.filename)

        procedure = self.make_procedure()
        results = Results(procedure, filename)
        experiment = self.new_experiment(results)

        self.manager.queue(experiment)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
sys.exit(app.exec_())