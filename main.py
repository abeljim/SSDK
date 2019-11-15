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

'''
def burst(A,st)
    sh("gphoto2 --capture-image-and-download --interval=1 --frames=5 --force-overwrite")
    sh("mv *.jpg ~/Pictures/tmp")
    i = st
    for filename in os.listdir("~/Pictures/tmp")
        dst = "capt" + str(A) + str(i)+ "jpg"
        src = '~/Pictures/tmp' + filename
        dst = '~/Pictures/tmp' + dst
        os.rename(src,dst)
        i + = 1
'''    

# Currents to be tested
i = [0.00005, 0.000100,0.000250]

# image capture loop
for j in range(3): # number of replicates
    for k in range((len(i)-1)): # counts currents
        # Prime the Electrode
        keithley.source_i(sourcemeter, I=0.001)
        sourcemeter.write(':OUTP ON')
        countdown(60)
        signal()
        sourcemeter.write('OUTP OFF')
        countdown(120)
        
        # Reaching SS
        print("reaching SS")
        keithley.source_i(sourcemeter,I = i[k]) # set current
        sourcemeter.write('OUTP ON') # run current
        countdown(300) # 5 minutes
        signal() # signals SS is reached
        
        # Capture SS Images
        number = ssdk_pb2.Number(value=1)
        response = stub.TakePhoto(number)
        sh("gphoto2 --capture-image-and-download --interval=2 --frames=150 --force-overwrite")
        sh("mv *.jpg ~/Pictures/" + str(i[k]) + "_S" + str(j))
        signal() # signals SS images are captured
        
        ## Capture Decay Images
        """
        sourcemeter.write('OUTP OFF')
        sh("gphoto2 --capture-image-and-download --interval=1 --frames=120 --force-overwrite")
        sh("mv *.jpg ~/Pictures/" + str(i[k]) + "_S" + str(j))
        sh("gphoto2 --capture-image-and-download --interval=1 --frames=120 --force-overwrite")
        sh("mv *.jpg ~/Pictures/tmp")
        burst(0,121)
        sh("mv ~/Pictures/tmp/*.jpg ~/Pictures/" + str(i[k]) + "_S" + str(j))
        """

        sourcemeter.write('OUTP OFF')
        sh("../scripts/capture2.sh " + "~/Pictures/" + str(i[k]) + "_S" + str(j)) 




        
