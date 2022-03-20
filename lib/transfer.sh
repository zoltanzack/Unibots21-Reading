#!/bin/bash

src=~/.local/lib/python3.7/site-packages/
dst=~/robotics-competition/Unibots21-Reading/lib/

contents=(adafruit_blinka adafruit_bus_device adafruit_motor adafruit_pca9685.py Adafruit_PureIO adafruit_register adafruit_servokit.py)

for i in "${contents[@]}"
do
	cp -r $src$i $dst$i
done
