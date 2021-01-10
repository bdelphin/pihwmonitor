import subprocess
import time

ip = '192.168.42.1/24'

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
