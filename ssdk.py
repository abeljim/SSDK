import math
import os

def sh(script):
    os.system("bash -c '%s'" % script)

def take_photo(x):
	sh("gphoto2 --capture-image-and-download")
	return 0
