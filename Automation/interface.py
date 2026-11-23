# WAP to check Interface IP on any router by any user

from netmiko import ConnectHandler
from getpass import getpass

username = input("Enter Username : ")
pwd = getpass("Enter Password : ")
ip = input("Enter Router IP : ")

device = {
    "device_type": "cisco_ios",
    "host": ip,
    "username": username,
    "password": pwd
}

ssh = ConnectHandler(**device)

output = ssh.send_command("show ip int brief")

print(output)

ssh.disconnect()



#ROUTER CONFIGURATION TO ENABLE SSH

'''
enable
configure terminal

hostname R1

! Configure management interface
interface GigabitEthernet0/0
 ip address 192.168.1.220 255.255.255.0
 no shutdown
 exit

! Configure SSH
ip domain-name lab.local

username admin privilege 15 secret Cisco123!

crypto key generate rsa modulus 1024

ip ssh version 2

line vty 0 4
 login local
 transport input ssh
 exit

end
write memory

'''

