#WAP to get information from router

import paramiko
import time

#Router List:
routers = [
    "192.168.1.220",
    "192.168.1.221",
    "192.168.1.222"
]


# Show Commands List
show_commands = [
    "show ip interface brief",
    "show ip route",
    "show ip arp",
    "show ip ospf neighbor",
    "show version"
]


for ip in routers:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(username="admin", password="cisco@123", hostname=ip)
        print("Connected Successfully")

        shell = ssh.invoke_shell()
        time.sleep(2)

        #clear intial router output
        while shell.recv_ready():
            shell.recv(65535)

        #disables pagination. the \n = the same as pressing enter in the terminal
        shell.send("terminal length 0\n")
        time.sleep(1)

        while shell.recv_ready():
            shell.recv(65535)

        for command in show_commands:
            print("\n Executing:", command)
            shell.send(command + "\n")
            time.sleep(2)
            output = ""

            #buffer size to return device info
            while shell.recv_ready():
                router_output = shell.recv(65535).decode()
                output += router_output

            print(output)

    except Exception as router_error:
        print("Execution Failed", ip)
        print(router_error)

    finally:
        ssh.close()
