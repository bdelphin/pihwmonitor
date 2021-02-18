import wmi

w = wmi.WMI(namespace="root\OpenHardwareMonitor")

def getComponents():
    "Return OpenHardware components list (with each component sensors)"
    sensors = []
    hardware = []

    complete_list = []

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

    orphan_components = []

    # loop through components
    for component in hardware:
        if component['parent'] != '':     
            orphan_components.append({ "identifier": component['identifier'], "name": component['name'], "parent": component['parent']})
        else:
            for orphan in orphan_components:
                if component['identifier'] == orphan['parent']:
                    dict = {}
                    dict['ComponentName'] = component['name']
                    dict['ComponentType'] = component['type']
                    dict['ComponentSensors'] = []
                    #print("\n═╦═ "+component['name']+' ('+component['identifier']+' - '+component['type']+')')
                    #print(" ╚═╦═ "+orphan['name']+' ('+orphan['identifier']+')')                
                    for sensor in sensors:
                        if sensor['parent'] == orphan['identifier']:
                            sensor_dict = {}
                            sensor_dict['SensorName'] = sensor['name']
                            sensor_dict['SensorType'] = sensor['type']
                            sensor_dict['SensorValue'] = sensor['value']
                            if sensor['type'] == "Temperature":
                                sensor_dict['SensorUnit'] = '°C'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' °C')
                            elif sensor['type'] == "Load" or sensor['type'] == "Control" or sensor['type'] == "Level":
                                sensor_dict['SensorUnit'] = '%'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' %')
                            elif sensor['type'] == "Clock":
                                sensor_dict['SensorUnit'] = 'MHz'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' MHz')
                            elif sensor['type'] == "Fan":
                                sensor_dict['SensorUnit'] = 'RPM'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' RPM')
                            elif sensor['type'] == "Flow":
                                sensor_dict['SensorUnit'] = 'L/h'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' L/h')
                            elif sensor['type'] == "Voltage":
                                sensor_dict['SensorUnit'] = 'V'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' V')
                            elif sensor['type'] == "Data":
                                sensor_dict['SensorUnit'] = 'GB'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' GB')
                            elif sensor['type'] == "Power":
                                sensor_dict['SensorUnit'] = 'W'
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' W')
                            elif sensor['type'] == "Factor":
                                sensor_dict['SensorUnit'] = ''
                                #print("   ╠═══ "+sensor['name']+' : '+str(sensor['value']))
                            else:
                                #print("   ╠═══ "+'unknown sensor type : '+sensor['type'])
                            dict['ComponentSensors'].append(sensor_dict)
                    complete_list.append(dict)
            else:
                #print("\n═╦═ "+component['name']+' ('+component['identifier']+' - '+component['type']+')')
                dict = {}
                dict['ComponentName'] = component['name']
                dict['ComponentType'] = component['type']
                dict['ComponentSensors'] = []
                for sensor in sensors:
                    if sensor['parent'] == component['identifier']:
                        sensor_dict = {}
                        sensor_dict['SensorName'] = sensor['name']
                        sensor_dict['SensorType'] = sensor['type']
                        sensor_dict['SensorValue'] = sensor['value']
                        if sensor['type'] == "Temperature":
                            sensor_dict['SensorUnit'] = '°C'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' °C')
                        elif sensor['type'] == "Load" or sensor['type'] == "Control" or sensor['type'] == "Level":
                            sensor_dict['SensorUnit'] = '%'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' %')
                        elif sensor['type'] == "Clock":
                            sensor_dict['SensorUnit'] = 'MHz'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' MHz')
                        elif sensor['type'] == "Fan":
                            sensor_dict['SensorUnit'] = 'RPM'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' RPM')
                        elif sensor['type'] == "Flow":
                            sensor_dict['SensorUnit'] = 'L/h'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' L/h')
                        elif sensor['type'] == "Voltage":
                            sensor_dict['SensorUnit'] = 'V'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' V')
                        elif sensor['type'] == "Data":
                            sensor_dict['SensorUnit'] = 'GB'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' GB')
                        elif sensor['type'] == "Power":
                            sensor_dict['SensorUnit'] = 'W'
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value'])+' W')
                        elif sensor['type'] == "Factor":
                            sensor_dict['SensorUnit'] = ''
                            #print(" ╠═══ "+sensor['name']+' : '+str(sensor['value']))
                        else:
                            #print('unknown sensor type : '+sensor['type'])
                        dict['ComponentSensors'].append(sensor_dict)
                complete_list.append(dict)

    # delete nodes without sensors :
    for i in range(len(complete_list)-1, -1, -1):
        if len(complete_list[i]['ComponentSensors']) == 0:
            del complete_list[i]

    return complete_list

def print():
    "Print OpenHardware components list (with each component sensors)"

    complete_list = getComponents()

    for component in complete_list:
        print('\nComponent: '+component['ComponentName'])
        print('Type: '+component['ComponentType'])
        print('Sensors : ')
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Temperature':
                print('  Temperatures:')
                print('    '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Load':
                print('  Load:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Clock':
                print('  Clocks:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Voltage':
                print('  Voltages:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Power':
                print('  Powers:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Data':
                print('  Data:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Fan':
                print('  Fans:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Control':
                print('  Controls:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Level':
                print('  Levels:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
        for sensor in component['ComponentSensors']:
            if sensor['SensorType'] == 'Factor':
                print('  Factors:')
                print('   '+sensor['SensorName']+': '+sensor[SensorValue]+' '+sensor[SensorUnit])
