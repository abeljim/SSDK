import math
import os

def sh(script):
    os.system("bash -c '%s'" % script)

def take_photo(x, name):
        if(x == 1):
            sh("gphoto2 --capture-image-and-download --force-overwrite --interval=1 --frames=300")
        elif(x == 2):
            sh("mkdir /home/sierra/Pictures/" + str(name))
            sh("sh ./capture2.sh " + str(name))
