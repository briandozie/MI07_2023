from flask import Blueprint, request
from utilities.databaseFunc import *
import nmap
import subprocess
import os
import signal
import xml.etree.ElementTree as ET

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")
pid = 0
cancelled = False

@ipScan.post("/")
def scanIpAddress():
    data = request.get_json()
    scanTypeLabel = data["scanTypeLabel"]

    if "ipAddress" in data:
        return ipScanSingle(data, scanTypeLabel)

    elif "ipAddresses" in data:
        return ipScanMultiple(data, scanTypeLabel)

    elif "ipRange" in data:
        return ipScanRange(data, scanTypeLabel)

    else:
        return "Invalid request format"
    
def ipScanSingle(data, scanTypeLabel):
    global pid, cancelled
    ipAddress = data["ipAddress"]
    subnetMask = data["subnetMask"]

    # retrieve command from database
    command = getCommand("IPSCAN", "SINGLE")
    command = command.format(
        ipAddress=ipAddress,
        subnetMask=subnetMask
    )

    process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    pid = process.pid
    output, _ = process.communicate()  # Wait for the process to finish and get the output

    if not cancelled:
        hostList = formatScanResult(output)
        logActivity("IP SCAN SINGLE", ipAddress + "/" + subnetMask, scanTypeLabel, hostList)
        return hostList
    else:
        cancelled = False
        return {}, 204

def ipScanMultiple(data, scanTypeLabel):
    global pid, cancelled
    hostList = []  # Initialize a list to store IP addresses

    # retrieve command from database
    command = getCommand("IPSCAN", "MULTIPLE")

    for ipAddress in data["ipAddresses"]:
        finalCommand = command.format(ipAddress=ipAddress)
        process = subprocess.Popen(finalCommand, shell=True, text=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
        pid = process.pid
        output, _ = process.communicate()  # Wait for the process to finish and get the output

        # Format the scan result using the function
        if not cancelled:
            hostList.extend(formatScanResult(output))
        else:
            break

    if not cancelled:
        logActivity("IP SCAN MULTIPLE", data["ipAddresses"], scanTypeLabel, hostList)
        return hostList
    else:
        cancelled = False
        return {}, 204


def ipScanRange(data, scanTypeLabel):
    global pid, cancelled
    startIP, endIP = data["ipRange"].split("-")

    # retrieve command from database
    command = getCommand("IPSCAN", "RANGE")
    command = command.format(
        startIP=startIP,
        endIP=endIP
    )

    # scan network for hosts
    process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    pid = process.pid
    output, _ = process.communicate()  # Wait for the process to finish and get the output

    if not cancelled:
        # Format the scan result using the function
        hostList = formatScanResult(output)
        logActivity("IP SCAN RANGE", data["ipRange"], scanTypeLabel, hostList)
        return hostList
    else:
        cancelled = False
        return {}, 204
    
def formatScanResult(output):
    # Parse the XML data
    root = ET.fromstring(output)

    # Create a list to store IP addresses
    ip_addresses = []

    # Iterate over each host in the XML
    for host in root.findall(".//host"):
        # Extract IP address
        ip_address = host.find(".//address").get('addr')
        ip_addresses.append(ip_address)

    return ip_addresses

@ipScan.get("/cancel")
def cancelScan():
    global pid, cancelled
    os.killpg(pid, signal.SIGTERM)
    cancelled = True
    return "activity cancelled"
