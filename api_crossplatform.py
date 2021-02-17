from flask import Flask
from flask_cors import CORS, cross_origin

import os
import platform
import psutil
import subprocess
import wmi

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def api():
    # if under Unix/Linux/OSX :
    if os.name != 'nt':
        # Temps (keys : nvme, k10temp, amdgpu)
        temps = psutil.sensors_temperatures()
        # Fans (only GPU) 
        fans = psutil.sensors_fans()
        # Watercooling
        h2o = subprocess.check_output('/usr/bin/liquidctl status', shell=True)
    # if under Windows
    elif os.name == 'nt':
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        sensors = []
        for sensor in w.Sensor():
            dict = {}
            dict['name'] = sensor.Name
            dict['value'] = sensor.Value
            dict['type'] = sensor.SensorType
            sensors.append(dict)

    # RAM
    ram = psutil.virtual_memory()
    # Disk usage
    for part in psutil.disk_partitions():
        if part.mountpoint == '/' or part.mountpoint == 'C:\\':
            diskusage = psutil.disk_usage(part.mountpoint)
    
    json = '{'
    
    if os.name == 'nt':
        json += '"hostname": "'+subprocess.check_output("hostname", shell=True).decode("utf-8")[:-2]+'",'
        json += '"system": "'+platform.system()+' '+platform.win32_ver()[0]+'",'
    else:
        json += '"hostname": "'+subprocess.check_output("hostname", shell=True).decode("utf-8")[:-1]+'",'
        json += '"system": "'+subprocess.check_output("uname -or", shell=True).decode("utf-8")[:-1]+'",'
    

    if os.name == 'nt':
        json += '"components": ['

        json += '{'
        json += '"label": "GPU - RX5700 XT",'
        json += '"probe": ['
        json += '{ "type": "temp", "name": "no data", "current": "no data", "high": "no data", "critical": "no data" },'
        json += '{ "type": "percent", "name": "gpu load", "current": "no data"},'
        json += '{ "type": "percent", "name": "vram usage", "current": "no data"},'
        #json += '{ "type": "ram_usage", "name": "vram used/total", "current": "'+"{:.2f}".format(float(subprocess.check_output("tail -n1 /tmp/radeontop.log", shell=True).decode("utf-8").split(", ")[12].split(" ")[2][:-2])/1000)+'", "max": "8"},'
        json += '{ "type": "fan", "name": "fan", "current": "no data", "max": "???"}'
        json += ']'
        json += '},'

        json += '{'
        json += '"label": "CPU - Ryzen5 3600XT",'
        json += '"probe": ['
        json += '{ "type": "temp", "name": "no data", "current": "no data", "high": "no data", "critical": "no data" },'
        json += '{ "type": "percent", "name": "Load", "current": "'+str(psutil.cpu_percent(interval=None))+'"},'
        json += '{ "type": "freq", "name": "Freq", "current": "'+"{:.2f}".format(psutil.cpu_freq().current/1000)+'", "max": "'+format(psutil.cpu_freq().max/1000)+'"}'
        json += ']'
        json += '},'

        json += '{'
        json += '"label": "Watercooling - H100i",'
        json += '"probe": ['
        json += '{ "type": "temp", "name": "no data", "current": "no data", "high": "40", "critical": "60" },'
        json += '{ "type": "fan", "name": "no data", "current": "no data", "max": "???"},'
        json = json[:-1]
        json += ']'
        json += '},'

        json += '{'
        json += '"label": "Others",'
        json += '"probe": ['
        json += '{ "type": "percent", "name": "RAM Usage", "current": "'+str(ram.percent)+'"},'
        #json += '{ "type": "percent", "name": "Disk Usage", "current": "'+diskspace[4][:-1]+'"},'    
        json += '{ "type": "percent", "name": "Disk Usage", "current": "'+str(diskusage.percent)+'"},'    
        json += '{ "type": "temp", "name": "no data", "current": "no data", "high": "no data", "critical": "no data" },'    
        json += '{ "type": "ram_usage", "name": "RAM Used/Total", "current": "'+psutil._common.bytes2human(ram.total-ram.available)[:-1]+'", "max": "'+psutil._common.bytes2human(ram.total)[:-1]+'"}'
        json += ']'
        json += '}'

        json += ']'
        json += '}'

    else:
        json += '"components": ['

        json += '{'
        json += '"label": "GPU - RX5700 XT",'
        json += '"probe": ['
        for probe in temps['amdgpu']:
            json += '{ "type": "temp", "name": "'+probe.label+'", "current": "'+str(probe.current)+'", "high": "'+str(probe.high)+'", "critical": "'+str(probe.critical)+'" },'
        json += '{ "type": "percent", "name": "gpu load", "current": "'+subprocess.check_output("tail -n1 /tmp/radeontop.log", shell=True).decode("utf-8").split(", ")[1].split(" ")[1][:-1]+'"},'
        json += '{ "type": "percent", "name": "vram usage", "current": "'+subprocess.check_output("tail -n1 /tmp/radeontop.log", shell=True).decode("utf-8").split(", ")[12].split(" ")[1][:-1]+'"},'
        #json += '{ "type": "ram_usage", "name": "vram used/total", "current": "'+"{:.2f}".format(float(subprocess.check_output("tail -n1 /tmp/radeontop.log", shell=True).decode("utf-8").split(", ")[12].split(" ")[2][:-2])/1000)+'", "max": "8"},'
        json += '{ "type": "fan", "name": "fan", "current": "'+str(fans['amdgpu'][0].current)+'", "max": "???"}'
        json += ']'
        json += '},'

        json += '{'
        json += '"label": "CPU - Ryzen5 3600XT",'
        json += '"probe": ['
        for probe in temps['k10temp']:
            json += '{ "type": "temp", "name": "'+probe.label+'", "current": "'+str("{:.1f}".format(probe.current))+'", "high": "'+str(probe.high)+'", "critical": "'+str(probe.critical)+'" },'
        json += '{ "type": "percent", "name": "Load", "current": "'+str(psutil.cpu_percent(interval=None))+'"},'
        json += '{ "type": "freq", "name": "Freq", "current": "'+"{:.2f}".format(psutil.cpu_freq().current/1000)+'", "max": "'+format(psutil.cpu_freq().max/1000)+'"}'
        json += ']'
        json += '},'

        json += '{'
        json += '"label": "Watercooling - H100i",'
        json += '"probe": ['
        for probe in h2o.decode().split('\n')[1:5]:
            if 'temperature' in probe:
                json += '{ "type": "temp", "name": "'+probe[4:10]+'", "current": "'+probe[26:30]+'", "high": "40", "critical": "60" },'
            else:
                json += '{ "type": "fan", "name": "'+probe[4:10]+'", "current": "'+probe[26:30]+'", "max": "???"},'
        json = json[:-1]
        json += ']'
        json += '},'

        json += '{'
        json += '"label": "Others",'
        json += '"probe": ['
        json += '{ "type": "percent", "name": "RAM Usage", "current": "'+str(ram.percent)+'"},'
        #json += '{ "type": "percent", "name": "Disk Usage", "current": "'+diskspace[4][:-1]+'"},'    
        json += '{ "type": "percent", "name": "Disk Usage", "current": "'+str(diskusage.percent)+'"},'    
        json += '{ "type": "temp", "name": "'+temps['nvme'][0].label+'", "current": "'+str("{:.1f}".format(temps['nvme'][0].current))+'", "high": "'+str(temps['nvme'][0].high)+'", "critical": "'+str(temps['nvme'][0].critical)+'" },'    
        json += '{ "type": "ram_usage", "name": "RAM Used/Total", "current": "'+psutil._common.bytes2human(ram.total-ram.available)[:-1]+'", "max": "'+psutil._common.bytes2human(ram.total)[:-1]+'"}'
        json += ']'
        json += '}'

        json += ']'
        json += '}'

    return json

if __name__ == '__main__':
    app.run(host='0.0.0.0')


