import sys
import subprocess
import configparser
import requests
import time

# Load config file
config = configparser.ConfigParser()
config.read('config.ini')

# Grab subnet from config file and generate host IP
subnet = config['GLOBAL']['Subnet']
ip = subnet.split('/')[0]
ip = ip.split('.')[0] + '.' + ip.split('.')[1] + '.' + ip.split('.')[2] + '.' + str(int(ip.split('.')[3]) + 2)

ip = '192.168.42.5'

# check arguments supplied
if len(sys.argv) == 2:
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        if arg == '--reboot' or arg == '--shutdown' or arg == '--reload':
            print('Sending', arg[2:], 'command ... ', end='')
            time.sleep(1)
            out = subprocess.check_output('/usr/bin/curl -s http://' + ip + ':5000/' + arg[2:], shell=True)
            #out = requests.get('http://' + ip + ':5000/' + arg[2:])
            if out == 'NOK':
                print("ERROR.\n Unable to send command.")
            else:
                print('OK.')
        elif arg == '-h' or arg == '--help':
            print('rpi_control.py : Python script for sending remote commands to RPi.')
            print('This script is part of PiHWMonitor : https://github.com/bdelphin/pihwmonitor.')
            print('Available arguments are --reboot, --shutdown')
            exit(1)
        else:
            print('Error, unrecognized argument.')
            print('Valid arguments are --reboot, --shutdown')
            print('Use -h or --help for more info.')
            exit(1)

elif len(sys.argv) > 2:
    print('Error, please send only one argument at a time !')
    print('Available arguments are --reboot, --shutdown')
    print('Use -h or --help for more info.')
    exit(1)

else:
    # no argument supplied
    print('Error, please provide an argument !')
    print('Available arguments are --reboot, --shutdown')
    print('Use -h or --help for more info.')
    exit(1)

