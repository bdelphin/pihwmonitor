import wmi

class HardwareInfos():
    "OpenHardwareMonitor Class"

    w = wmi.WMI(namespace="root\OpenHardwareMonitor")

    def getComponents(self):
        "Return OpenHardware components list (with each component sensors)"
        sensors = []
        hardware = []

        complete_list = []

        for component in self.w.Hardware():
            dict = {}
            dict['name'] = component.Name
            dict['identifier'] = component.Identifier
            dict['type'] = component.HardwareType
            dict['parent'] = component.Parent
            hardware.append(dict)

        for sensor in self.w.Sensor():
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
                        for sensor in sensors:
                            if sensor['parent'] == orphan['identifier']:
                                sensor_dict = {}
                                sensor_dict['SensorName'] = sensor['name']
                                sensor_dict['SensorType'] = sensor['type']
                                sensor_dict['SensorValue'] = sensor['value']
                                if sensor['type'] == "Temperature":
                                    sensor_dict['SensorUnit'] = '°C'
                                elif sensor['type'] == "Load" or sensor['type'] == "Control" or sensor['type'] == "Level":
                                    sensor_dict['SensorUnit'] = '%'
                                elif sensor['type'] == "Clock":
                                    sensor_dict['SensorUnit'] = 'MHz'
                                elif sensor['type'] == "Fan":
                                    sensor_dict['SensorUnit'] = 'RPM'
                                elif sensor['type'] == "Flow":
                                    sensor_dict['SensorUnit'] = 'L/h'
                                elif sensor['type'] == "Voltage":
                                    sensor_dict['SensorUnit'] = 'V'
                                elif sensor['type'] == "Data":
                                    sensor_dict['SensorUnit'] = 'GB'
                                elif sensor['type'] == "Power":
                                    sensor_dict['SensorUnit'] = 'W'
                                elif sensor['type'] == "Factor":
                                    sensor_dict['SensorUnit'] = ''
                                dict['ComponentSensors'].append(sensor_dict)
                        complete_list.append(dict)
                else:
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
                            elif sensor['type'] == "Load" or sensor['type'] == "Control" or sensor['type'] == "Level":
                                sensor_dict['SensorUnit'] = '%'
                            elif sensor['type'] == "Clock":
                                sensor_dict['SensorUnit'] = 'MHz'
                            elif sensor['type'] == "Fan":
                                sensor_dict['SensorUnit'] = 'RPM'
                            elif sensor['type'] == "Flow":
                                sensor_dict['SensorUnit'] = 'L/h'
                            elif sensor['type'] == "Voltage":
                                sensor_dict['SensorUnit'] = 'V'
                            elif sensor['type'] == "Data":
                                sensor_dict['SensorUnit'] = 'GB'
                            elif sensor['type'] == "Power":
                                sensor_dict['SensorUnit'] = 'W'
                            elif sensor['type'] == "Factor":
                                sensor_dict['SensorUnit'] = ''
                            dict['ComponentSensors'].append(sensor_dict)
                    complete_list.append(dict)

        # delete nodes without sensors :
        for i in range(len(complete_list)-1, -1, -1):
            if len(complete_list[i]['ComponentSensors']) == 0:
                del complete_list[i]

        return complete_list

    def print(self):
        "Print OpenHardware components list (with each component sensors)"

        complete_list = self.getComponents()

        for component in complete_list:
            print('\nComponent: '+component['ComponentName'])
            print('Type: '+component['ComponentType'])
            print('Sensors : ')
            print('  Temperatures:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Temperature':                
                    print('    '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Load:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Load':       
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Clocks:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Clock': 
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Voltages:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Voltage':
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Powers:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Power':
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Data:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Data':
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Fans:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Fan':
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Controls:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Control':
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Levels:')
            for sensor in component['ComponentSensors']:
                if sensor['SensorType'] == 'Level':
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
            print('  Factors:')
            for sensor in component['ComponentSensors']:         
                if sensor['SensorType'] == 'Factor':
                    print('   '+sensor['SensorName']+': '+str(sensor['SensorValue'])+' '+sensor['SensorUnit'])
