#!/bin/bash


# UNFINISHED !! #		# 5/8/2018
# maybe find a better way to check if port 1340 is open
# perhaps just check if the process is running or not ?
# this script should also return true or false (0/1) to make it easier
# for other scripts to use it (like amionline.sh)

# UPDATE 			# 30/11/2018
# Changed the check to be better, now it is based on 
# the return value from the is-active request
# if zero, then 1 is returned (as in "true")
# if not zero is returned, return 0 as in "false"

ANS=$(systemctl is-active myserver1.service)
if [[ "$?" -eq "0" ]]; then
	# if 0 was reutned, all is well - return 1 as in "true"
	echo "1"
else
	# if not 0 was returned, return 0 as in false
	echo "0"
fi;

