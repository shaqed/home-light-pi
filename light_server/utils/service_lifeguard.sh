#!/bin/bash

# this is the script to be used on the cron 
# as it documents everything its doing to a log file

LOG_FILE="../log/online_status.txt"

ANS=$(./is_service_up.sh)

if [ "$?" -ne 8 ]; then
	date >> $LOG_FILE
	./is_service_up.sh >> $LOG_FILE
	echo "------------" >> $LOG_FILE
else
	echo "not doing anything"

fi
