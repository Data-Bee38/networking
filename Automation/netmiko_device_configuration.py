"""
Cisco IOS multi-router automation lab using Netmiko.

Install:  py -m pip install netmiko
Run:      py netmiko_menu.py

Edit routers.txt first. Put one router management IP/hostname per line.

MAKE SURE THE ROUTERS HAVE THE CORRECT USERNAME, PASSWORD & PRIVILEGE
"""

from getpass import getpass
from pathlib import Path

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

ROUTER_FILE = Path(__file__).with_name("routers.txt")


def load_routers():
    if not ROUTER_FILE.exists():
        print(f"Missing {ROUTER_FILE.name}. Create it beside this script.")
        return []

    with ROUTER_FILE.open(encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.lstrip().startswith("#")
        ]


def connect_to_router(host, username, password):
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
        "secret": password,
        "fast_cli": False,
    }

    print(f"\nConnecting to {host}...")
    try:
        connection = ConnectHandler(**device)
        connection.enable()
        print(f"Connected successfully to {host}.")
        return connection
    except NetmikoAuthenticationException:
        print(f"Authentication failed for {host}.")
    except NetmikoTimeoutException:
        print(f"Connection timed out to {host}. Check IP and SSH connectivity.")
    except Exception as error:
        print(f"Could not connect to {host}: {error}")
    return None


def show_command(connection):
    command = input("\nEnter a show command (e.g. show ip int brief): ").strip()
    if not command:
        print("No command entered.")
        return
    try:
        print(connection.send_command(command))
    except Exception as error:
        print(f"Command failed: {error}")


def configure_interface(connection):
    name = input("Enter interface name (e.g. GigabitEthernet0/0): ").strip()
    ip = input("Enter interface IP address: ").strip()
    mask = input("Enter subnet mask: ").strip()
    description = input("Enter interface description: ").strip()

    if not name or not ip or not mask:
        print("Interface name, IP address, and subnet mask are required.")
        return

    commands = [
        f"interface {name}",
        f"ip address {ip} {mask}",
        "no shutdown",
    ]
    if description:
        commands.append(f"description {description}")

    try:
        print(connection.send_config_set(commands))
    except Exception as error:
        print(f"Interface configuration failed: {error}")


def configure_ospf(connection):
    try:
        process_id = int(input("Enter OSPF process ID: ").strip())
    except ValueError:
        print("OSPF process ID must be a number.")
        return

    network = input("Enter network ID (e.g. 192.168.1.0): ").strip()
    wildcard = input("Enter wildcard mask (e.g. 0.0.0.255): ").strip()
    area = input("Enter OSPF area ID: ").strip()

    if not network or not wildcard or not area:
        print("Network, wildcard mask, and area are required.")
        return

    commands = [
        f"router ospf {process_id}",
        f"network {network} {wildcard} area {area}",
    ]
    try:
        print(connection.send_config_set(commands))
    except Exception as error:
        print(f"OSPF configuration failed: {error}")


def router_menu(connection, host):
    while True:
        print(f"\n========== Connected to {host} ==========")
        print("1. Execute a show command")
        print("2. Configure an interface")
        print("3. Configure OSPF")
        print("4. Exit this router")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            show_command(connection)
        elif choice == "2":
            configure_interface(connection)
        elif choice == "3":
            configure_ospf(connection)
        elif choice == "4":
            print(f"Leaving {host}.")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


def main():
    routers = load_routers()
    if not routers:
        print("No routers listed. Edit routers.txt and try again.")
        return

    print("Cisco IOS Netmiko Automation Lab")
    print("Routers found:")
    for host in routers:
        print(f"  - {host}")

    username = input("\nSSH username [admin]: ").strip() or "admin"
    password = getpass("SSH password: ")

    for host in routers:
        connection = connect_to_router(host, username, password)
        if connection is None:
            continue

        try:
            router_menu(connection, host)
        finally:
            connection.disconnect()
            print(f"Disconnected from {host}.")

    print("\nFinished processing router list.")


if __name__ == "__main__":
    main()
