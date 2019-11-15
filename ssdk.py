import math
import os

def sh(script):
    os.system("bash -c '%s'" % script)

def take_photo(x):
        if(x == 1):
            sh("gphoto2 --capture-image-and-download")
        elif(x == 2):
            sh("sh ./capture2.sh")
            
	return 0
