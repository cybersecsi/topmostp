from pathlib import Path
from datetime import datetime
from time import sleep
from enum import Enum
import os
import requests
import csv

# Vars
NMAP_SERVICE_SOURCE = "https://raw.githubusercontent.com/nmap/nmap/master/nmap-services" # We use the 'nmap-services' file to get the list of ports
class TopPortsTypeArg(str, Enum):
    tcp = "tcp"
    udp = "udp"
    sctp = "sctp"
    all = "all"
class PortTypeArg(str, Enum):
    tcp = "tcp"
    udp = "udp"
    sctp = "sctp"

# Colors
SUCCESS_C = '\033[92m'
DEBUG_C = '\033[93m'
ERROR_C = '\033[91m'
BOLD = '\033[1m'
END_C = '\033[0m'

def banner():
  print(
    '''
    ███████╗███████╗ ██████╗███████╗██╗
    ██╔════╝██╔════╝██╔════╝██╔════╝██║
    ███████╗█████╗  ██║     ███████╗██║
    ╚════██║██╔══╝  ██║     ╚════██║██║
    ███████║███████╗╚██████╗███████║██║
    ╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝
    topmostp v0.1.7 - https://github.com/cybersecsi/topmostp
    ''')   

def log(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}] - [LOG] - {msg}", flush=True)

def success(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{SUCCESS_C}[{current_time}] - [SUCCESS] - {msg}{END_C}", flush=True)

def err(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{ERROR_C}[{current_time}] - [ERROR] - {msg}{END_C}", flush=True)

def bold(msg):
    print(f"{BOLD}{msg}{END_C}", flush=True)

def get_config_file():
    home_folder = Path.home()
    return os.path.join(home_folder,'.config', 'topmostp', 'ports.csv')

def check_config_folder():
    home_folder = Path.home()
    config_folder = os.path.join(home_folder,'.config', 'topmostp')
    config_file = get_config_file()

    if not os.path.exists(config_folder):
        err("Missing config folder, creating it...")
        os.makedirs(config_folder)

    if not os.path.exists(config_file):
        err("Missing config file, creating it...")
        update_ports()

def update_ports():
    log(f"Connecting to '{NMAP_SERVICE_SOURCE}' to retrieve list of ports...")
    connection_successful = False
    while not connection_successful:
        nmap_services_res = requests.get(NMAP_SERVICE_SOURCE)
        if nmap_services_res.status_code == 200:
            connection_successful = True
            success("Connection successful")
        else:
            err("Connection error, retrying in 2 seconds...")
            sleep(2)

    nmap_services = nmap_services_res.text

    structured_ports = [{
        'service': line.split()[0], 
        'port': line.split()[1], 
        'frequency': line.split()[2]
    } for line in nmap_services.splitlines() if not line.startswith("#")]
    ordered_ports = sorted(structured_ports, key=lambda x: x["frequency"], reverse=True)

    with open(get_config_file(), 'w', newline='') as ports_file:
        writer = csv.writer(ports_file)
        for v in ordered_ports:
            row = [v["service"], v["port"], v["frequency"]]
            writer.writerow(row)
    success("Update completed!")

def get_ports(n: int, tcp: bool, udp: bool, sctp: bool):
    ports_list = []
    with open(get_config_file(), 'r') as ports_file:
        csv_reader = csv.reader(ports_file, delimiter=',')
        for row in csv_reader:
            port_type = row[1].split("/")[1]
            # Add port to the list
            if port_type == "tcp" and tcp:
                ports_list.append(row[1].split("/")[0])
            elif port_type == "udp" and udp:
                ports_list.append(row[1].split("/")[0])
            elif port_type == "sctp" and sctp:
                ports_list.append(row[1].split("/")[0])
            # Check if n is reached, remove duplicates and recheck (ugly but more performant)
            if n == len(ports_list):
                ports_list = list(dict.fromkeys(ports_list))
            if n == len(ports_list):
                break   
    return ports_list

def port_info(port: int, port_type: str):
    with open(get_config_file(), 'r') as ports_file:
        csv_reader = csv.reader(ports_file, delimiter=',')
        num_rows = len(ports_file.readlines())
        ports_file.seek(0)
        for i, row in enumerate(csv_reader):
            if int(row[1].split("/")[0]) == port and row[1].split("/")[1] == port_type:
                print(f"{BOLD}Service:{END_C} {row[0]}", flush=True)
                print(f"{BOLD}Port:{END_C} {row[1].split('/')[0]}", flush=True)
                print(f"{BOLD}Type:{END_C} {row[1].split('/')[1].upper()}", flush=True)
                print(f"{BOLD}Frequency:{END_C} {row[2]}", flush=True)
                print(f"{BOLD}Ranking:{END_C} {i+1}/{num_rows}", flush=True)
                return
    # If reaches this point it means the port was not found
    err("Port not found")

def find_services(service: str):
    match_found = False
    with open(get_config_file(), 'r') as ports_file:
        csv_reader = csv.reader(ports_file, delimiter=',')
        num_rows = len(ports_file.readlines())
        ports_file.seek(0)
        for i, row in enumerate(csv_reader):
            s = row[0]
            if service.lower() in s.lower():
                match_found = True
                success("Match found:")
                print(f"{BOLD}Service:{END_C} {row[0]}", flush=True)
                print(f"{BOLD}Port:{END_C} {row[1].split('/')[0]}", flush=True)
                print(f"{BOLD}Type:{END_C} {row[1].split('/')[1].upper()}", flush=True)
                print(f"{BOLD}Frequency:{END_C} {row[2]}", flush=True)
                print(f"{BOLD}Ranking:{END_C} {i+1}/{num_rows}", flush=True)   

    if not match_found:
        err("No match found")