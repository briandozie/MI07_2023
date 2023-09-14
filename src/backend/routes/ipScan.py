from flask import Blueprint, request
from utilities.databaseFunc import *
import nmap

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")

@ipScan.post("/")
def scanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    
    scanType = data["scanType"]

    if "ipAddress" in data:
        ipAddress = data["ipAddress"]
        subnetMask = data["subnetMask"]
        # scan network for hosts
        nm = nmap.PortScanner()
        nm.scan(hosts=f"{ipAddress}/{subnetMask}", arguments=f"-{scanType} -D RND:30")
        hostList = nm.all_hosts()

        logActivity("IP SCAN SINGLE", ipAddress + "/" + subnetMask, scanType, hostList)

        return hostList
    
    elif "ipAddresses" in data:
        # Scan multiple individual IP addresses
        ipAddresses = data["ipAddresses"]
        
        # scan network for hosts
        nm = nmap.PortScanner()
        hostList = []
        for ipAddress in ipAddresses:
            nm.scan(hosts=ipAddress, arguments=f"-{scanType} -D RND:30")
            hostList.extend(nm.all_hosts())

        logActivity("IP SCAN MULTIPLE", ipAddresses, scanType, hostList)

        return hostList
    
    elif "ipRange" in data:
        # Scan a range of IP addresses
        ipRange = data["ipRange"]
        startIP, endIP = ipRange.split("-")
        # scan network for hosts
        nm = nmap.PortScanner()
        nm.scan(hosts=f"{startIP}-{endIP}", arguments=f"-{scanType} -D RND:30")
        hostList = nm.all_hosts()

        logActivity("IP SCAN RANGE", ipRange, scanType, hostList)

        return hostList
    else:
        return "Invalid request format"