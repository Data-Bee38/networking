# WAP to configure a static route

from netmiko import ConnectHandler
from getpass import getpass

username = input("Enter Username : ")
pwd = getpass("Enter Password : ")
ip = input("Enter Router IP : ")

network	= input("Enter Destination Network :")
mask = input("Enter Subnet Mask : ")
next_hop = input("Enter Next-Hop IP : ")

device = {
    "device_type": "cisco_ios",
    "host": ip,
    "username": username,
    "password": pwd
}

ssh = ConnectHandler(**device)

command = {
    f"ip route {network} {mask} {next_hop}"
}
#GLOBAL CONFIG MODE
output = ssh.send_config_set(command)
print(output)
ssh.disconnect()


