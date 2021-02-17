import wmi

w = wmi.WMI(namespace="root\OpenHardwareMonitor")

sensors = []
hardware = []

for component in w.Hardware():
    dict = {}
    dict['name'] = component.Name
    dict['identifier'] = component.Identifier
    dict['type'] = component.HardwareType
    dict['parent'] = component.Parent
    hardware.append(dict)

for sensor in w.Sensor():
    dict = {}
    dict['name'] = sensor.Name
    dict['identifier'] = sensor.Identifier
    dict['type'] = sensor.SensorType
    dict['parent'] = sensor.Parent
    dict['value'] = sensor.Value
    sensors.append(dict)

orphan_component_identifier = ''
orphan_component_name = ''
orphan_component_parent = ''

for component in hardware:
    if component['parent'] != '':
        orphan_component_parent = component['parent']
        orphan_component_identifier = component['identifier']
        orphan_component_name = component['name']
    else:
        if component['identifier'] == orphan_component_parent:
            print("\n═╦═ "+component['name'])
            print(" ╚═╦═ "+orphan_component_name)
            for sensor in sensors:
                if sensor['parent'] == orphan_component_identifier:
                    if sensor['type'] == "Temperature":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' °C')
                    elif sensor['type'] == "Load" or sensor['type'] == "Control" or sensor['type'] == "Level":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' %')
                    elif sensor['type'] == "Clock":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' MHz')
                    elif sensor['type'] == "Fan":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' RPM')
                    elif sensor['type'] == "Flow":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' L/h')
                    elif sensor['type'] == "Voltage":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' V')
                    elif sensor['type'] == "Data":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' GB')
                    elif sensor['type'] == "Power":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' W')
                    elif sensor['type'] == "Factor":
                        print("   ╠═══ "+sensor['name']+' : '+str(sensor['value']))
                    else:
                        print("   ╠═══ "+'unknown sensor type : '+sensor['type'])
        else:
            print("\n═╦═ "+component['name'])
            #print("Parent: "+component['parent'])
            #print("Identifier: "+component['identifier'])
            for sensor in sensors:
                if sensor['parent'] == component['identifier']:
                    if sensor['type'] == "Temperature":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' °C')
                    elif sensor['type'] == "Load" or sensor['type'] == "Control" or sensor['type'] == "Level":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' %')
                    elif sensor['type'] == "Clock":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' MHz')
                    elif sensor['type'] == "Fan":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' RPM')
                    elif sensor['type'] == "Flow":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' L/h')
                    elif sensor['type'] == "Voltage":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' V')
                    elif sensor['type'] == "Data":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' GB')
                    elif sensor['type'] == "Power":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' W')
                    elif sensor['type'] == "Factor":
                        print(" ╠═══ "+sensor['name']+' : '+str(sensor['value']))
                    else:
                        print('unknown sensor type : '+sensor['type'])