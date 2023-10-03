from flask import Blueprint, request
from utilities.databaseFunc import *
import nmap
import subprocess
import os
import signal
import xml.etree.ElementTree as ET

serviceScan = Blueprint("serviceScan", __name__, url_prefix="/serviceScan")
pid = 0
cancelled = False

@serviceScan.post("/")
def ServiceScan():
    global pid, cancelled
    
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    
    # retrieve command from database
    command = getCommand("SERVICESCAN", scanType)
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
        logActivity("SERVICE SCAN", ipAddress, scanType, ports)

        return finalJson
    else:
        cancelled = False
        return {}, 204

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
                'port': port.get('portid'),
                'name': port.find(".//service").get('name'),
                'product': port.find(".//service").get('product'),
                'extrainfo': port.find(".//service").get('extrainfo'),
                'version': port.find(".//service").get('version')
            }
            ports.append(port_info)

    return ports

@serviceScan.get("/cancel")
def cancelScan():
    global pid, cancelled
    os.killpg(pid, signal.SIGTERM)
    cancelled = True
    return "activity cancelled"
