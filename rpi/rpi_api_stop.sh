#!/bin/sh

# Stop RPIAPI service.

# Find and kill Python API
/usr/bin/pgrep -f 'rpi_api.py' | /usr/bin/xargs /usr/bin/kill
/usr/bin/echo "Python API stopped."

/usr/bin/echo "RPiAPI service stopped."

