#!/bin/bash
WD="/home/sierra/Pictures/$1"
gphoto2 --capture-image-and-download --force-overwrite --interval=1 --frames=300
mv *.jpg $WD