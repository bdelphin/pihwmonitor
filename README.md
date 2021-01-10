# PiHWMonitor
## Raspberry Pi based hardware monitor

PiHWMonitor is an external hardware monitor for a computer, using a Raspberry Pi and a 5" display.

![screenshot](screenshot.png?raw=true "Screenshot")

## Host compatibility

PiHWMonitor aims to be cross-platform, you should soon be able to monitor your Windows or GNU/Linux system. For now, the host software is only designed for GNU/Linux.

It has been developed and tested on Arch Linux, but it should run on most GNU/Linux distributions.

For now, it's only designed to monitor AMD GPU stats. Nvidia GPU support should come soon (using https://github.com/wookayin/gpustat).

### Windows TODO-list :
- test psutil under windows (should work)
- test liquidctl under windows (should work)
- find a Radeontop alternative to monitor Radeon GPU under windows (possible candidate : https://github.com/GPUOpen-Tools/gpu_performance_api)
- automate USB OTG network configuration
- create a script which will be launched by a planned task at boot (or create a serice ?)
- create a setup.exe file, for automating the planned task creation

### GNU/Linux TODO-list :
- ~~modify otg_ip.py script, add permanent supervision of the OTG network interface (if it disappears, this means the Raspberry Pi has been unplugged and we need to watch for its reconnection)~~
- create an install script, which will create the systemd service
- nvidia GPU support (https://github.com/wookayin/gpustat)

### General TODO-list :
- ~~fix some gauges names~~
- config file (to specify components to monitor and subnet to use)
- ~~get ping stats and display it on the last gauge remaining~~ (finally no, SSD temperature is nice and don't require an internet connection)
- add a Flask Python API which will run on the RPi (to reboot & shutdown it easily)
- change subnet used (currently using 192.168.42.0/24, we don't need that much)
- bug fix : forever loading when the computer have no internet access (download gauge.js & google fonts ?)

### 

## How it works

PiHWMonitor is based on a Python "service" which is running on the computer you want to monitor. This Python script uses the psutil module to get CPU, RAM and disk stats. GPU stats comes from Radeontop and Watercooling stats from Liquidctl. 

A very basic API (only answers GET requests on /) is then making those hardware stats available in JSON format, using Flask Python module.

The Python script is started at boot by a systemd service.

On the Raspberry Pi, there's only an HTML/CSS/JS webpage display in a Chromium instance started in kiosk mode.
Every second, an HTTP GET request is sent from JS to get updated hardware stats. The JSON data received is then parsed and used to update the gauges.

### Links to software used in this project :
- https://bernii.github.io/gauge.js/#! for the gauges.
- https://github.com/giampaolo/psutil for CPU, RAM and disk stats.
- https://github.com/liquidctl/liquidctl for Watercooling stats.
- https://github.com/clbr/radeontop for GPU stats.

## Hardware used

Currently I'm using a Raspberry Pi model A+ which is painfully slow, even overclocked to 1ghz.
The RPi is connected to the host computer with a single USB typeA-typeA cable. That's made possible by the RPi A+ USB-OTG capability.

I should test the RPi 3 A+ soon, hoping it'll be much more faster.

The display used is a 5" Raspberry Pi HDMI monitor with resistive touchscreen. I'm not using the touchscreen at all for now, since it seems to cause an issue with USB-OTG. 

## How to build yours

Currently, PiHWMonitor is designed and will only work with AMD GPU. It should work with any Radeontop compatible AMD GPU. It's also currently designed to monitor an AIO liquid CPU cooler with liquidctl (find liquid cooler supported here : https://github.com/liquidctl/liquidctl#supported-devices).

Since it has only been tested on my computer, chances are high that even with an AMD GPU and a liquidctl compatible liquid CPU cooler it will not work flawlessly,

But, if you want to give it a try, please do ! (you can contact me for help if needed)

You'll need a USB-OTG compatible Raspberry Pi (candidates are : RPi 4, zero / zero W, 3A+ and A+) and a 5" display (800x480 resolution). A bigger display should work, but be aware that the webpage is designed for 800x480 resolution and will need adjustments to fit bigger resolutions. 
A smaller display would definitely be a bad idea for that purpose.

Ready ? Mount the display on your RPi and follow these steps (on your host computer) :
- install radeontop and liquidctl (they should be available in your disto's repos) 
- initialize liquidctl (follow instructions provided on the github page) and automate its launch with a systemd service
- clone my repo
- copy hwmonitor.service to /etc/systemd/system/
- edit hwmonitor.service : change ExecStart and ExecStop paths to fit the cloned repo location on your computer
- lauch "systemctl daemon-reload"
- flash the image on the sdcard
- test the service by running "systemctl start hwmonitor" and immediately connect the RPi to your computer.
- the service should hang, waiting for the USB OTG network interface detection. Once it ends, check service status by running "systemctl status hwmonitor".
- if you don't see any errors, and if the RPi is displaying your system stats correctly, you should be good to go. Enable hwmonitor service by running "systemctl enable hwmonitor". 

Those instructions will soon be updated as I'm still working on this project.

