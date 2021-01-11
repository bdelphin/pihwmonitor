import subprocess
import time
import configparser

# Load config file 
config = configparser.ConfigParser()
config.read('config.ini')

# Grab subnet from config file and generate host IP
subnet = config['GLOBAL']['Subnet']
ip = subnet.split('/')[0]
ip = ip.split('.')[0] + '.' + ip.split('.')[1] + '.' + ip.split('.')[2] + '.' + str(int(ip.split('.')[3]) + 1)
ip = ip + '/' + subnet.split('/')[1]

# ip = '192.168.42.1/24'

# check every 10 seconds if OTG IP is still assigned
# if not, relaunch otg_ip.py
while True:

    # when IP is assigned, 'ip a' command will list it, and the return code of that subprocess call should be 0
    if subprocess.run('ip a | grep '+ip, shell=True, stdout=subprocess.DEVNULL).returncode != 0:
        # if returncode != 0, ip is no longer assigned.
        print('Lost contact with OTG device. Trying to reassign IP ...')
        # launch otg_ip.py
        if subprocess.run('python /home/baptiste/Projects/PiHWMonitor/otg_ip.py -y', shell=True, stdout=subprocess.DEVNULL).returncode != 0:
            print('Unable to reassing IP. Retry in 10 secs.')
        else:
            print('IP successfully reassigned !')

    time.sleep(10)
