#!/usr/bin/env python3

from typing import List # To support Python>3.5
import typer
import topmostp.helper as helper

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})

def intro():
    helper.banner()
    helper.check_config_folder()

@app.command()
def update():
    """
        Update ports list
    """
    intro()
    helper.update_ports()

@app.command()
def top(n: int, type:List[helper.TopPortsTypeArg] = typer.Option(["all"], "--type", "-t"), silent: bool = typer.Option(False, "--silent", "-s", help="Display only results in output")):
    """
        Retrieve list of ports by frequency (TCP, UDP, SCTP or all of them. Defaults to 'all')
    """
    if not silent:
        intro()
        print("You can hide the previous output with the silent option (-s or --silent) or specify the port type you want to filter (-t or --type).")
        print("Run 'topmostp top -h' for more info.\n")

    tcp = False
    udp = False
    sctp = False
    if helper.TopPortsTypeArg.all in type:
        tcp = True
        udp = True
        sctp = True
    else:
        if helper.TopPortsTypeArg.tcp in type:
            tcp = True
        if helper.TopPortsTypeArg.udp in type:
            udp = True
        if helper.TopPortsTypeArg.sctp in type:
            sctp = True
    ports = helper.get_ports(n, tcp=tcp, udp=udp, sctp=sctp)
    print(",".join(ports))

@app.command()
def stats(port: int, port_type: helper.PortTypeArg):
    """
        Retrieve stats about a port
    """
    intro()
    helper.port_info(port, port_type.value)

@app.command()
def find(service: str):
    """
        Find info about about a specific service
    """
    intro()
    helper.find_services(service)