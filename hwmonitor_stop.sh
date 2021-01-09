#!/bin/sh

# Stop PiHWMonitor service.

# Find and kill Python API
/usr/bin/pgrep -f 'api.py' | /usr/bin/xargs /usr/bin/kill
/usr/bin/echo "Python API stopped."

# Find and kill radeontop dump
/usr/bin/pgrep -f '/tmp/radeontop.log' | /usr/bin/xargs /usr/bin/kill
/usr/bin/rm /tmp/radeontop.log
/usr/bin/echo "Radeontop dump stopped."

/usr/bin/echo "PiHWMonitor service stopped."

