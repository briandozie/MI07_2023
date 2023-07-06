from flask import Blueprint, request
import nmap

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")

@ipScan.post("/")
def scanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    scanType = data["scanType"]
    
    if "ipAddresses" in data:
        # Scan multiple individual IP addresses
        ipAddresses = data["ipAddresses"]
        
        # scan network for hosts
        nm = nmap.PortScanner()
        hostList = []
        for ipAddress in ipAddresses:
            nm.scan(hosts=ipAddress, arguments=f"-{scanType} --spoof-mac <your_mac_address>")
            hostList.extend(nm.all_hosts())
        return hostList
    
    elif "ipRange" in data:
        # Scan a range of IP addresses
        ipRange = data["ipRange"]
        startIP, endIP = ipRange.split("-")
        # scan network for hosts
        nm = nmap.PortScanner()
        nm.scan(hosts=f"{startIP}-{endIP}", arguments=f"-{scanType}")
        hostList = nm.all_hosts()
        return hostList
    else:
        return "Invalid request format"