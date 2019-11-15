import os
import visa
import keithley
import time
import numpy as np
import grpc
import ssdk_pb2
import ssdk_pb2_grpc

channel = grpc.insecure_channel('127.0.1.1:50051') 
stub = ssdk_pb2_grpc.CameraStub(channel)
rm = visa.ResourceManager()
rm.list_resources()
sourcemeter = rm.open_resource('GPIB0::12::INSTR')
keithley.initialize(sourcemeter)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        print('\n')
        time.sleep(1)
        t -= 1
def signal():
    sourcemeter.write('SYSTem:BEEPer 523.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 659.25,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 783.99,0.1')
    time.sleep(0.2)
    sourcemeter.write('SYSTem:BEEPer 1046.50,0.1')

def sh(script):
    os.system("bash -c '%s'" % script)


# Currents to be tested
i = [0.00005, 0.000100, 0.000250]

# image capture loop
for j in range(3): # number of replicates
    for k in range((len(i)-1)): # counts currents
        # Prime the Electrode
        keithley.source_i(sourcemeter, I=0.001)
        sourcemeter.write(':OUTP ON')
        countdown(60)
        sourcemeter.write('OUTP OFF')
        countdown(120)
        
        # Reaching SS
        print("reaching SS")
        keithley.source_i(sourcemeter,I = i[k]) # set current
        sourcemeter.write('OUTP ON') # run current
        countdown(300) # 5 minutes
                
        # Capture SS Images
        fname = str(str(int(i[k]*(1000000))) + '_S' + str(j))
        number = ssdk_pb2.Number(value=1,name=fname)
        stub.TakePhoto(number)
        
        ## Capture Decay Images
        fname = str(str(int(i[k]*(1000000))) + '_D' + str(j))
        number = ssdk_pb2.Number(value=2,name=fname)
        sourcemeter.write('OUTP OFF')
        stub.TakePhoto(number)
        print('done with current: ' + str(int(i[k]*(1000000))) + 'uA')
        




        
