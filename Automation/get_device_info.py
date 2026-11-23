
from netmiko import ConnectHandler
from getpass import getpass

# ==========================================
# DEVICE IP ADDRESSES
# ==========================================

device_list = [
    "192.168.1.202",
    "192.168.1.203",
    "192.168.1.204",
    "192.168.1.205"
]

# ==========================================
# COMMANDS TO EXECUTE
# ==========================================

command_list = [
    "show ip interface brief",
    "show ip route",
    "show ip arp",
    "show ip protocols"
]

# ==========================================
# LOGIN CREDENTIALS
# ==========================================

username = input("Enter the Username: ")
password = getpass("Enter the Password: ")
secret = getpass("Enter the Enable Secret: ")

# ==========================================
# CONNECT TO EACH ROUTER
# ==========================================

for host in device_list:

    print("\n===================================")
    print("Connecting to:", host)
    print("===================================")

    try:

        ssh = ConnectHandler(
            host=host,
            username=username,
            password=password,
            secret=secret,
            device_type="cisco_ios"
        )

        # Enter privileged EXEC mode
        ssh.enable()

        # Execute each command
        for command in command_list:

            print("\n")
            print("Router:", host)
            print("Command:", command)
            print("-----------------------------------")

            output = ssh.send_command(command)

            print(output)

        # Disconnect from router
        ssh.disconnect()

    except Exception as e:

        print("Connection failed to:", host)
        print("Error:", e)

print("\nAll devices processed!")
