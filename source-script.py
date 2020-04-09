''' IMPORTS '''

import json
import requests
import dateparser
import base64
import urllib3
import ipaddress

# Disable insecure warnings
requests.packages.urllib3.disable_warnings()

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


## Base function

class Client():
    def __init__(self,url,verify,user,password):
        self.url = url
        self.user = user
        self.password = password
        self.verify = verify


    def test_connection(self,client):
        user = client.user
        password = client.password
        url = client.url + "/api/v1.0/login"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        user = base64.b64encode(user.encode('utf-8')).decode("utf-8")
        password = base64.b64encode(password.encode('utf-8')).decode("utf-8")

        session = requests.Session()

        auth_headers = {
            'Authorization': 'KSCBasic user="' + user + '", pass="' + password + '", internal="1"',
            'Content-Type': 'application/json',
        }

        data = {}

        response = session.post(url=client.url, headers=auth_headers, data=data, verify=False)
        code = response.status_code
        return(code)

    def find_host(self,client,ipaddress):
        session = requests.Session()

        ##Start Authentication
        user = client.user
        password = client.password
        url = client.url + "/api/v1.0/login"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        user = base64.b64encode(user.encode('utf-8')).decode("utf-8")
        password = base64.b64encode(password.encode('utf-8')).decode("utf-8")

        auth_headers = {
            'Authorization': 'KSCBasic user="' + user + '", pass="' + password + '", internal="1"',
            'Content-Type': 'application/json',
        }

        data = {}
        response = session.post(url=client.url, headers=auth_headers, data=data, verify=False)
        ##End Authentication


        ##Query for data
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        common_headers = {
            'Content-Type': 'application/json',
        }
        url = client.url + "/api/v1.0/HostGroup.FindHosts"

        data = {"wstrFilter": "(KLHST_WKS_IP_LONG = " + str(ipaddress) + ")",
                "vecFieldsToReturn": ['KLHST_WKS_DN', 'KLHST_WKS_WINHOSTNAME', 'KLHST_WKS_WINDOMAIN', 'KLHST_WKS_OS_NAME'], "lMaxLifeTime": 100}
        response = session.post(url=url, headers=common_headers, data=json.dumps(data), verify=False)

        if 'strAccessor' in json.loads(response.text):
            strAccessor = json.loads(response.text)['strAccessor']
            url = client.url + "/api/v1.0/ChunkAccessor.GetItemsCount"
            common_headers = {
                'Content-Type': 'application/json',
            }
            data = {"strAccessor": strAccessor}
            response = session.post(url=url, headers=common_headers, data=json.dumps(data), verify=False)
            items_count = json.loads(response.text)['PxgRetVal']

            start = 0
            step = 100000
            results = list()
            while start < items_count:
                url = client.url + "/api/v1.0/ChunkAccessor.GetItemsChunk"
                data = {"strAccessor": strAccessor, "nStart": 0, "nCount": items_count}
                response = session.post(url=url, headers=common_headers, data=json.dumps(data), verify=False)
                results += json.loads(response.text)['pChunk']['KLCSP_ITERATOR_ARRAY']
                start += step
            hosts = results
            for host in hosts:
                print("Host name: " + host['value']['KLHST_WKS_WINHOSTNAME'] + " OS is: " + host['value']['KLHST_WKS_OS_NAME'])



## Demisto command
def test_module(client):
    result = client.test_connection(client)
    if result == 200:
        return 'ok'
    else:
        return 'error'


def find_ip_command(client,ip):
    print('Searching host information for requested IP address..')
    client.find_host(client,ip)


## Main program to call command
def main():
    url = demisto.params().get('url')
    user = demisto.params().get('credentials').get('identifier')
    password = demisto.params().get('credentials').get('password')
    verify_certificate = not demisto.params().get('insecure', False)
    proxy = demisto.params().get('proxy', False)

    LOG(f'Command being called is {demisto.command()}')
    try:
        client = Client(
            url=url,
            verify=verify_certificate,
            user=user,
            password=password)

        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module(client)
            demisto.results(result)

        elif demisto.command() == 'kasper-find-ip':
            ip = int(ipaddress.ip_address(demisto.args().get('ip')))
            #return_outputs(find_ip_command(client, ip))
            find_ip_command(client,ip)

    # Log exceptions
    except Exception as e:
        return_error(f'Failed to execute {demisto.command()} command. Error: {str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
