#!/usr/bin/env python3

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
def all(n: int, silent: bool = typer.Option(False, "--silent", "-s")):
    """
        Retrieve list of all ports (both TCP, UDP and SCTP) by frequency
    """
    if not silent:
        intro()
        print("You can hide the previous output with the silent option (-s or --silent)")   
    ports = helper.get_ports(n, tcp=True, udp=True, sctp=True)
    print(",".join(ports))

@app.command()
def tcp(n: int, silent: bool = typer.Option(False, "--silent", "-s")):
    """
        Retrieve list of TCP ports by frequency
    """
    if not silent:
        intro()
        print("You can hide the previous output with the silent option (-s or --silent)")
    ports = helper.get_ports(n, tcp=True, udp=False, sctp=False)
    print(",".join(ports))

@app.command()
def udp(n: int, silent: bool = typer.Option(False, "--silent", "-s")):
    """
        Retrieve list of UDP ports by frequency
    """
    if not silent:
        intro()
        print("You can hide the previous output with the silent option (-s or --silent)")
    ports = helper.get_ports(n, tcp=False, udp=True, sctp=False)
    print(",".join(ports))

@app.command()
def sctp(n: int, silent: bool = typer.Option(False, "--silent", "-s")):
    """
        Retrieve list of SCTP ports by frequency
    """
    if not silent:
        intro()
        print("You can hide the previous output with the silent option (-s or --silent)")
    ports = helper.get_ports(n, tcp=False, udp=False, sctp=True)
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