from flask import Blueprint, request
from utilities.databaseFunc import *
from utilities.utilities import *
import nmap
import subprocess
import os
import signal
import xml.etree.ElementTree as ET

portScan = Blueprint("portScan", __name__, url_prefix="/portScan")
pid = 0
cancelled = False

@portScan.post("/")
def PortScan():
    global pid, cancelled

    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]

    if isHostReachable(ipAddress):
    
        # retrieve command from database
        command = getCommand("PORTSCAN", scanType)
        command = command.format(
            ipAddress = ipAddress
        )

        process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
        pid = process.pid
        output, _ = process.communicate() # Wait for the process to finish and get the output

        if not cancelled:
            ports = formatScanResult(output)

            # Calculate the total number of items
            totalNumber = len(ports)

            # Create the final JSON structure
            finalJson = {'ports': ports, 'total': totalNumber}
            logActivity("PORT SCAN", ipAddress, scanType, ports)

            return finalJson
        else:
            cancelled = False
            return {}, 204
        
    else:
        return {}, 400

def formatScanResult(output):
   # Parse the XML data
    root = ET.fromstring(output)
    
    # Create a list to store dictionaries for each port
    ports = []

    # Iterate over each host in the XML
    for host in root.findall(".//host"):
        host_info = {}

        # Extract host information
        host_info['address'] = host.find(".//address").get('addr')

        # Iterate over each port in the host
        for port in host.findall(".//port"):
            port_info = {
                'host': host_info['address'],
                'protocol': port.get('protocol'),
                'port': port.get('portid'),
                'status': port.find(".//state").get('state')
            }
            ports.append(port_info)

    return ports

@portScan.get("/cancel")
def cancelScan():
    global pid, cancelled
    os.killpg(pid, signal.SIGTERM)
    cancelled = True
    return "activity cancelled"
