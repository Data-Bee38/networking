
from netmiko import ConnectHandler

file = open("routers.txt", "r")
data = file.readlines()

for host in data:
    host = host.strip()

    ssh = ConnectHandler(
        username="admin",
        password="cisco@123",
        host=host,
        device_type="cisco_ios"
    )

    while True:
        print("you are connected to router", host)
        print("1. Want to Execute any Show Command :\n"
              "2. Want to configure any interface :\n"
              "3. Want to Configure OSPF :\n"
              "4. Exit")

        ch = int(input("Enter Your Choice :"))

        if ch == 1:
            command = input("Enter any Show Command :")
            output = ssh.send_command(command)
            print(output)

        elif ch == 2:
            int_name = input("Enter Interface name :")
            int_ip = input("Enter Interface IP :")
            int_mask = input("Enter Subnet Mask :")
            int_desc = input("Enter Interface Description :")

            int_config = [
                f"interface {int_name}",
                f"ip address {int_ip} {int_mask}",
                f"no shutdown",
                f"descr {int_desc}"
            ]

            output = ssh.send_config_set(int_config)
            print(output)

        elif ch == 3:
            ospf_process_id = int(input("Enter ospf process-id :"))
            ospf_network = input("Enter Network-id :")
            ospf_wildcard = input("Enter Wildcard Mask :")
            ospf_area = input("Enter OSPF Area-id")

            ospf_config = [
                f"router ospf {ospf_process_id}",
                f"network {ospf_network} {ospf_wildcard} area {ospf_area}"
            ]

            output = ssh.send_config_set(ospf_config)
            print(output)

        elif ch == 4:
            break
