import requests
import json

USER = 'devnetuser'
PASSWORD = 'Cisco123!'
AUTH = requests.auth.HTTPBasicAuth(USER, PASSWORD)
AUTH_RESPONSE = requests.post('https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token', auth=AUTH, verify=False)

TOKEN = json.loads(AUTH_RESPONSE.text)['Token']

HEADERS = { 'X-Auth-Token': TOKEN }

BASE_URL = 'https://sandboxdnac.cisco.com/dna/intent/api/v1'
RESOURCE = '/network-device'

call_response = requests.get(BASE_URL + RESOURCE, headers=HEADERS, verify=False)
devices = json.loads(call_response.text)['response']

for device in devices:
    RESOURCE = '/interface/network-device/{deviceId}'.format(deviceId= device['id'])
    call_response = requests.get(BASE_URL + RESOURCE, headers=HEADERS, verify=False)
    interfaces = json.loads(call_response.text)['response']
    interfacesWithOSPF = []

    for interface in interfaces:
        if interface['ospfSupport'] == 'true':
            interfacesWithOSPF.append(interface)

    if len(interfacesWithOSPF) > 0:
        print('Interfaces with enabled OSPF on {hostname}:'.format(hostname=device['hostname']))

        for interface in interfacesWithOSPF:
            print('\t Name: {name}, IP: {ip}'.format(name=interface['portName'],
                                                     ip=interface['ipv4Address']))
    else:
        print('There are no interfaces with enabled OSPF on {hostname}'.format(hostname=device['hostname']))
