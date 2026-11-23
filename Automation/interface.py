# WAP to check Interface IP on any router by any user

from netmiko import ConnectHandler
from getpass import getpass

username = input("Enter Username : ")
pwd = getpass("Enter Password : ")
ip = input("Enter Router IP : ")

interface = input("Enter Interface Name : ")
interface_ip = input("Enter Interface IP : ")
mask = input("Enter Subnet Mask : ")

device = {
    "device_type": "cisco_ios",
    "host": ip,
    "username": username,
    "password": pwd
}

ssh = ConnectHandler(**device)

command = {
    f"interface {interface}",
    f"ip address {interface_ip} {mask}",
    f"no shutdown"
}
#GLOBAL CONFIG MODE
output = ssh.send_config_set(command)
print(output)
ssh.disconnect()

