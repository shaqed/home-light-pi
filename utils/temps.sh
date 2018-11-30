#!/bin/bash

# This script is used to measure the temperature
# of the board and record that to a file 
# The file will be in a JSON format.

# Get temperature of the board
#/opt/vc/bin/vcgencmd measure_temp

MAIN_DIR="/home/pi/light_server/log"

TEMP_FILE="$MAIN_DIR/temps_new.txt"

printf "{" >> $TEMP_FILE
printf "\"date\"" >> $TEMP_FILE  # date key
printf ": " >> $TEMP_FILE # ":"
printf "\"" >> $TEMP_FILE # starting "
printf "%s" "$(date +"%d/%m/%y %H:%M:%S")" >> $TEMP_FILE

printf "\"" >> $TEMP_FILE     # ending "

printf "," >> $TEMP_FILE # , for the next key-value item  

printf "\"temp\"" >> $TEMP_FILE # string "temp" for the key 
printf ": \""   >> $TEMP_FILE # : "...
printf "%s" "$(/opt/vc/bin/vcgencmd measure_temp)"  >> $TEMP_FILE 

printf "'\"}" >> $TEMP_FILE  # ending " and ending } of the json item
printf ",\n" >> $TEMP_FILE 
