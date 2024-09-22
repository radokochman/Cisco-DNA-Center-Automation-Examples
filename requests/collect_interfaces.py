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

    print('Interfaces on {hostname}:'.format(hostname=device['hostname']))

    for interface in interfaces:
        print('\tName: {name}, Status: {status}, Port mode: {portMode}, '
              'Speed: {speed}'.format(name=interface['portName'],
                                      status=interface['status'],
                                      portMode=interface['portMode'],
                                      speed=interface['speed']))
