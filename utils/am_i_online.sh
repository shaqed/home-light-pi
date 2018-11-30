#!/bin/bash

# EDITED ON 19/10/18
# Switched from pinging the home router to google.com
# Because sometimes there is connection to the router but none to the
# outside internet and when that happens
# other devices on the network cannot see this device (weird)
ANS=$(ping -c 5 google.com)

echo $?
