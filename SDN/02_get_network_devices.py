#import necessary modules for script to run correctly

import json
import requests

# define the API endpoint we want to query

#api_url = "http://192.168.101.254/api/v1/network-device"
api_url = "http://localhost:58000/api/v1/network-device"

# supply our authentication token in the request header 
# replace the <your_serviceTicket text in between the quotes with 
# the service ticket you obtained from running script 01_get_ticket.py

headers = {

    "X-Auth-Token": "NC-32-b8b0ca20e86c40529ede-nbi"
}

# execute our query

resp = requests.get(api_url, headers=headers, verify=False)

# print our request status code

print("Request status: ", resp.status_code)

# gather our response details

response_json = resp.json()

networkDevices = response_json["response"]

# loop through all the objects retrieved and print them on the screen

"""
#Returns the result in a list
hosts = response_json["response"]
results = []
for host in hosts:
    results.append(host)

print(results)
"""

for networkDevice in networkDevices:
    print(networkDevice["hostname"], "\t", networkDevice["platformId"], "\t", networkDevice["managementIpAddress"])
    print("\r \n")

# be a good corporate citizen and clean up after ourselves

resp = None
response_json = None
networkDevices = None
