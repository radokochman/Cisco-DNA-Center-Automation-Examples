from dnacentersdk import api

dnac = api.DNACenterAPI(username="devnetuser",
                        password="Cisco123!",
                        base_url="https://sandboxdnac.cisco.com",
                        verify=False)

devices = dnac.devices.get_device_list()

for device in devices['response']:
    print('Hostname: {hostname}, Type: {type}, MAC: {mac}, Serial: {serial}'.format(serial=device['serialNumber'],
                                                                                    hostname=device['hostname'],
                                                                                    type=device['type'],
                                                                                    mac=device['macAddress']))

device_mapping = {}

for device in devices['response']:
    device_mapping[device['id']] = device['hostname']


interfaces = dnac.devices.get_all_interfaces()
interfaces_by_device = {}

for interface in interfaces['response']:
    if interface['deviceId'] in interfaces_by_device.keys():
        interfaces_by_device[interface['deviceId']].append(interface)
    else:
        interfaces_by_device[interface['deviceId']] = [interface]

for device in interfaces_by_device:
    print('Interfaces on {hostname}:'.format(hostname=device_mapping[device]))
    for interface in interfaces_by_device[device]:
        print('\tName: {name}, Status: {status}, Port mode: {portMode}, '
              'Speed: {speed}'.format(name=interface['portName'],
                                      status=interface['status'],
                                      portMode=interface['portMode'],
                                      speed=interface['speed']))


ospf_interfaces = dnac.devices.get_ospf_interfaces()

ospf_interfaces_by_device = {}

for interface in ospf_interfaces['response']:
    if interface['deviceId'] in ospf_interfaces_by_device.keys():
        ospf_interfaces_by_device[interface['deviceId']].append(interface)
    else:
        ospf_interfaces_by_device[interface['deviceId']] = [interface]

for device in ospf_interfaces_by_device:
    print('Interfaces with enabled OSPF on {hostname}:'.format(hostname=device_mapping[device]))
    for interface in ospf_interfaces_by_device[device]:
        print('\t Name: {name}, IP: {ip}'.format(name=interface['portName'],
                                                 ip=interface['ipv4Address']))
