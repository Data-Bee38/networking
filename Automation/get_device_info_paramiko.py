#WAP to get information from router

import paramiko
import time

# Create SSH client object
ssh = paramiko.SSHClient()

ip = input("Enter Device IP :")
device = {
    "hostname": ip,
    "username": "admin",
    "password": "cisco@123"
}

# Taking care of fingerprint message --> Accept
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print(f"Connecting to {ip}")
ssh.connect(**device)

#/n = presing enter in terminal
shell = ssh.invoke_shell()
shell.send("terminal length 0\n")
shell.send("show run\n")
shell.send("show ip int brief\n")
shell.send("show ip arp\n")

#set timeout
time.sleep(1)

#set buffer size to recieve data back from device
output = shell.recv(65535).decode()
print(output)

if ssh.get_transport().is_active():
    print("Closing Connection")
    ssh.close()
