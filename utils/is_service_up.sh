#!/bin/bash

ONLINE_STATUS="/home/pi/light_server/log/online_status.txt"

# Checks if you can ping the home router 
PING=$(/home/pi/light_server/utils/am_i_online.sh)
if [ $PING -eq 0 ] ; then
	ONLINE=1
else
	ONLINE=0
fi;


SERV=$(/home/pi/light_server/utils/is_port_open.sh) 
if [ $ONLINE -eq 0 ]; then  # If we're not online
	date >> $ONLINE_STATUS
	if [ $SERV -eq 0 ]; then
		echo "ERR: Not online AND service isn't running, probably should reboot" >> $ONLINE_STATUS
	else
		echo "ERR: Not online but service is active rebooting, checkout info below:" >> $ONLINE_STATUS
		sudo systemctl status myserver1.service
	fi;
	echo "" >> $ONLINE_STATUS
	sleep 1m && sudo reboot
else
	if [ $SERV -eq 0 ]; then
		date >> $ONLINE_STATUS
		echo "ERR: You're online but service isn't running, restarting service" >> $ONLINE_STATUS
		echo "" >> $ONLINE_STATUS
		sudo systemctl restart myserver1.service
	else
		# disable when finished
		echo "You're online and service is running... we're all good!" >> $ONLINE_STATUS
	fi;	
fi;

