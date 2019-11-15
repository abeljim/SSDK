#!/bin/bash
WD = "/home/sierra/Pictures/$1"
epoch=$(date +%s%N)
counter=1
while [ $counter -le 10 ]; do
	echo $counter
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite 
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	counter=`expr $counter + 1`
done

counter=1
while [ $counter -le 10 ]; do

	echo $counter
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)

	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	counter=`expr $counter + 1`
	sleep 1s
done

counter=1
while [ $counter -le 10 ]; do
	echo $counter
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	counter=`expr $counter + 1`
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	sleep 10s
done

while [ $counter -le 20 ]; do
	echo $counter
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	counter=`expr $counter + 1`
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	time=$(expr $(date +%s%N) - $epoch)
	time=$(expr $time / 1000000)
	gphoto2 --capture-image-and-download --force-overwrite
	j=$(printf "%010d" $time)
	mv capt0000.jpg $WD/image_$j.jpg
	sleep 100s
done
notify-send  'Photos collected!'
