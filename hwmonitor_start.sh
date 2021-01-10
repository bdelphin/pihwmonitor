#!/bin/sh

# PiHWMonitor - A simple Hardware Monitor
# Python service : basic JSON API (Flask) communicating with a Raspberry Pi
# Displays various CPU, GPU, RAM, Watercooling statistics
#
# Aims to be cross-platform with the use of psutil & liquidcfg
# In search for a Radeontop-like solution for a windows full port
#
# https://baptistedelphin.fr

# Start Radeontop dump
/usr/bin/radeontop -d /tmp/radeontop.log > /tmp/radeontop_dump.log 2>&1 &
/usr/bin/echo "Radeontop dump started."

# Start Python Flask API
/usr/bin/python /home/baptiste/Projects/PiHWMonitor/api.py > /tmp/api.log 2>&1 &
/usr/bin/echo "Python Flask API started."

# Assign IP to USB OTG
/usr/bin/python /home/baptiste/Projects/PiHWMonitor/otg_ip.py -y
/usr/bin/echo "USB OTG IP assigned."

# Monitor OTG IP (if device reboot, reassign)
/usr/bin/python /home/baptiste/Projects/PiHWMonitor/check_otg.py &

/usr/bin/echo "PiHWMonitor service launched."
