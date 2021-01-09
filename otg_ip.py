import subprocess
import time
import os
import sys


# check arguments supplied
if len(sys.argv) != 1:
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        if arg == '-y' or arg == '--yes':
            force_yes = True
        elif arg == '-h' or arg == '--help':
            print('otg_ip.py : Python script for sharing internet access to USB OTG device.')
            print('Launch without argument to run in normal mode.')
            print('Use -y or --yes to use in a script (force firewall rules creation and select first active interface as the output.)')
            exit(1)
        else:
            print('Unrecognized argument. Please use « python otg_ip.py -h » or « python otg_ip.py --help » to show help screen.')
            exit(1)
else:
    # no argument supplied, running in normal mode
    force_yes = False


# TODO: create a config file and get ip from there
ip = '192.168.42.1/24'
subnet = '192.168.42.0/24'
int_name = ''

print('Starting USB OTG internet sharing utility', end='')
if force_yes:
    print(' in automatic mode.')
else:
    print('.\nPlease note that your computer should obviously have access to the internet itself.\n')

# check if IP is already assigned
# when IP is assigned, 'ip a' command will list it, and the return code of that subprocess call should be 0
if subprocess.run('ip a | grep '+ip, shell=True, stdout=subprocess.DEVNULL).returncode != 0:
    # loop while USB OTG isn't detected (10 tries)
    tries = 0
    while subprocess.run("lsusb | grep 'Linux-USB Ethernet/RNDIS Gadget'", shell=True, stdout=subprocess.DEVNULL).returncode != 0:
        tries += 1
        if tries > 9:
            print("Can't find any USB OTG device connected to your computer. Exiting.")
            exit(1)
        print('USB OTG device not found, retrying in 5 seconds ...')
        time.sleep(5)

    print('USB OTG device detected !\n')

    # check dmesg for USB OTG interface name
    # last entry containing 'renamed from usb' should be our USB OTG device
    int_name = subprocess.check_output("dmesg | grep 'renamed from usb0' | tail -1 | awk '{print $4}' | sed 's/.$//'", shell=True).decode('utf-8')

    # sometimes dmesg line is different, so let's check if int_name is correct
    if 'enp' not in int_name:
        # awk print $4 returned the wrong part of dmesg string, let's try $5
        int_name = subprocess.check_output("dmesg | grep 'renamed from usb0' | tail -1 | awk '{print $5}' | sed 's/.$//'", shell=True).decode('utf-8')

    # final check, if int_name is still bad, quit
    if 'enp' not in int_name:
        print('ERROR: Unable to get interface name.\nPlease check "dmesg | grep \'renamed from usb0\' | tail -1" command output and report a bug.')
        exit(1)

    # interface name should be the right one by now !
    # TODO: check if this interface doesn't already have an IP, that may be the case if there are multiple USB OTG devices connected.

    # remove newline char (\n) from interface name
    int_name = int_name[:-1]
    print('USB OTG interface name found:', int_name)

    # wait a sec, to be sure the interface is ready to be set
    time.sleep(1)

    # bring interface UP (should be down, TODO: check if that's the case ?)
    if subprocess.run('ip link set up dev '+int_name, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode != 0:
        try:
            subprocess.check_output('ip link set up dev '+int_name, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            print('ERROR: Unable to bring interface up.\nPlease report a bug and provide this error message:', err.output.decode('utf-8'))
            exit(1)

    print('USB OTG interface UP.')

    # set interface IP
    if subprocess.run('ip addr add 192.168.42.1/24 dev '+int_name, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode != 0:
        try:
            subprocess.check_output('ip addr add 192.168.42.1/24 dev '+int_name, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            print('ERROR: Unable to set interface IP.\nPlease report a bug and provide this error message:', err.output.decode('utf-8'))
            exit(1)

    print('Interface IP succesfully assigned.\n')

else:
    # IP address already assigned, let's check & display to which interface
    int_name = subprocess.check_output("ip a | grep '192.168.42.1/24' | awk '{print $5}'", shell=True).decode('utf-8') 
    # remove newline character (\n)
    int_name = int_name[:-1]
    print('IP address', ip, 'already assigned to', int_name, '!\nIf this address is already in use on your computer, please change host_ip parameter in config file.\n')

# if we are in normal mode (force_yes = False), ask the user if we should set firewall rules
if not force_yes:
    if input('Should we set firewall rules ? (Y/n) ') == 'n':
        # if he answer no, quit
        print('Skipped firewall rules creation.')
        exit(0)
    
# activate IP Forward
try:
    subprocess.check_output('sysctl net.ipv4.ip_forward=1', shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as err:
    print('ERROR: Unable to activate IP forwarding.\nPlease report a bug and provide this error message:', err.output.decode('utf-8'))
    exit(1)
#sysctl net.ipv4.ip_forward=1

print("IP forwarding activated.")

# For setting up firewall rules, we need to find active LAN/WLAN interface

# find UP interfaces :
active_int = subprocess.check_output("ip a | grep 'state UP' | awk '{print $2}' | sed 's/.$//'", shell=True).decode('utf-8')
# split by \n, since there may be more than one active interface
active_int = active_int.split('\n')
# remove empty elements from list
active_int = list(filter(None, active_int))

# check list length
if len(active_int) > 1 and not force_yes:
    # more than one interface is active AND we are in normal mode (force_yes = False)
    # so ask the user to choose which one to use
    print(len(active_int), 'active interfaces detected.')
    hint = '('
    for (index, interface) in enumerate(active_int):
        print(index,':',interface)
        hint += index + '/'
    hint = hint[:-1] + ')'
    choice = input('To which interface should we redirect USB OTG network traffic ?'+hint+' ')

    # test if the index selected by the user is correct, if not loop
    while choice not in enumerate(active_int).keys():
        print('Error, wrong interface index choosen !')
        choice = input('To which interface should we redirect USB OTG network traffic ?'+hint+' ')
    
    out_int = active_int[choice]
else:
    # only one interface active or script mode, select the first interface found
    out_int = active_int[0]

# Firewall rules
try:
    subprocess.check_output('iptables -t nat -A POSTROUTING -s '+subnet+' -o '+out_int+' -j MASQUERADE', shell=True, stderr=subprocess.STDOUT)
    subprocess.check_output('iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT', shell=True, stderr=subprocess.STDOUT)
    subprocess.check_output('iptables -A FORWARD -i '+int_name+' -o '+out_int+' -j ACCEPT', shell=True, stderr=subprocess.STDOUT)
    subprocess.check_output('iptables -I INPUT -p udp --dport 67 -i '+int_name+' -j ACCEPT', shell=True, stderr=subprocess.STDOUT)
    subprocess.check_output('iptables -I INPUT -p udp --dport 53 -i '+int_name+' -j ACCEPT', shell=True, stderr=subprocess.STDOUT)
    subprocess.check_output('iptables -I INPUT -p tcp --dport 53 -i '+int_name+' -j ACCEPT', shell=True, stderr=subprocess.STDOUT)
    subprocess.check_output('iptables -I INPUT -p tcp --dport 5000 -i '+int_name+' -j ACCEPT', shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as err:
    print('ERROR: Unable to set firewall rules.\nPlease report a bug and provide this error message:', err.output.decode('utf-8'))
    exit(1)

print('Firewall rules : OK.')
print('\nUSB OTG setup completed without errors. Your device should have internet access !')




# PREVIOUS CODE :

# backup & clear dmesg
# subprocess.check_output('dmesg > dmesg-`date +%d%m%Y`.log', shell=True)
# subprocess.check_output('dmesg -c', shell=True)
# print('dmesg backed up and cleared.')

# # look for USB OTG interface name 
# int_name = subprocess.check_output("dmesg | grep 'renamed from usb0' | tail -1 | awk '{print $4}' | sed 's/.$//'", shell=True).decode('utf-8')


# while (int_name == ''):
#     int_name = subprocess.check_output("dmesg | grep 'renamed from usb0' | tail -1 | awk '{print $4}' | sed 's/.$//'", shell=True).decode('utf-8')
#     time.sleep(2)
#
# print('OTG Interface found :', int_name)
#
# time.sleep(1)
#
# # set interface UP
# subprocess.check_output('ip link set up dev '+int_name, shell=True)
#
# print('OTF interface activated.')
#
# # set interface IP
# subprocess.check_output('ip addr add 192.168.42.1/24 dev '+int_name, shell=True)
#
# time.sleep(2)
#
# # check IP assigned
# ip = subprocess.check_output("ip a | grep -EA1 '"+int_name+"' | grep inet | awk '{print $2}'", shell=True).decode('utf-8')
# print('Succesfully assigned', ip, 'to interface',int_name,'!')
