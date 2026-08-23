ipaddr=input("Enter the IP Address or Domain Name of router: ")
uname=input("Enter a router username: ")
pword=input("Enter the password for the user "+uname+": ")
portno=input("Enter the port number to be used: ")
lono=input("Enter the number of the Loopback interface: ")
intdesc=input("Enter the description of the interface: ")
intip=input("Enter the IPv4 address of interface Loopback"+lono+": ")
intmask=input("Enter the subnet mask of interface Loopback"+lono+": ")
import requests
import json

from pprint import pprint

device = {
   "ip": ipaddr,
   "username": uname,
   "password": pword,
   "port": portno,
}

headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json", 
   }

module = "ietf-interfaces:interfaces"

url = f"https://{device['ip']}:{device['port']}/restconf/data/{module}"

payload = {
   "interface": [
    {
      "name": "Loopback"+lono,
      "description": intdesc,
      "type": "iana-if-type:softwareLoopback",
      "enabled": "true",
      "ietf-ip:ipv4": {
        "address": [
          {
            "ip": intip,
            "netmask": intmask
          }
        ]
      }
    }
  ]
 }
requests.packages.urllib3.disable_warnings()
response = requests.post(url, headers=headers, data=json.dumps(payload), auth=(device['username'], device['password']), verify=False)

if (response.status_code == 201):
   print("Successfully added interface")
else:
   print("Issue with adding interface")