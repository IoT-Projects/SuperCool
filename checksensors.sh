#!/bin/bash
#
# This script looks through your DS1820B devices and checks that they are functioning properly.
#
# YES or NO Provided
#
#
devlocation=/sys/bus/w1/devices

cd $devlocation 

oursensors=($(ls -d */))
i=0

for value in "${oursensors[@]}"
do
	if [[ $value == 28* ]]
	then 
		echo "Sensor $i" 
		cat "$devlocation/$value/w1_slave" | grep "crc" | sed -r 's/^.{36}//'
		i=$(($i+1))
	fi 
done
