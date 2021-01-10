#!/bin/sh

# PiHWMonitor - A simple Hardware Monitor
# Python service : basic JSON API (Flask) communicating with a Raspberry Pi
# Displays various CPU, GPU, RAM, Watercooling statistics
#
# Aims to be cross-platform with the use of psutil & liquidcfg
# In search for a Radeontop-like solution for a windows full port
#
# https://baptistedelphin.fr

# Start Python Flask API
/usr/bin/python3 /home/pi/rpi_api.py &
/usr/bin/echo "Python Flask API started."

/usr/bin/echo "RPiAPI service launched."
