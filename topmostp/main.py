#!/usr/bin/env python3

import typer
import topmostp.helper as helper

app = typer.Typer(add_completion=False)

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
def all(n: int, silent: bool = typer.Option(False, "--silent")):
    """
        Retrieve list of all ports (both TCP and UDP) by frequency
    """
    if not silent:
        intro()
    ports = helper.get_ports(n, tcp=True, udp=True)
    print(",".join(ports))

@app.command()
def tcp(n: int, silent: bool = typer.Option(False, "--silent")):
    """
        Retrieve list of TCP ports by frequency
    """
    if not silent:
        intro()
    ports = helper.get_ports(n, tcp=True, udp=False)
    print(",".join(ports))

@app.command()
def udp(n: int, silent: bool = typer.Option(False, "--silent")):
    """
        Retrieve list of UDP ports by frequency
    """
    if not silent:
        intro()
    ports = helper.get_ports(n, tcp=False, udp=True)
    print(",".join(ports))

@app.command()
def stats(port: int, port_type: helper.PortTypeArg):
    """
        Retrieve stats about a port
    """
    intro()
    helper.port_info(port, port_type.value)

